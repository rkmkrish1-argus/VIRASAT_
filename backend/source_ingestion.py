"""Public-catalog metadata connectors for the institutional archive.

Only descriptive metadata and links to the source repositories are imported.
The source files themselves remain hosted by their owning institutions.
"""

from __future__ import annotations

import hashlib
import html
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


DAF_CATALOG_URL = "https://ambedkarfoundation.nic.in/publication.html"
CAD_COLLECTION_URL = "https://eparlib.sansad.in/handle/123456789/760448/browse?type=date"
NDLI_INFO_URL = "https://project.ndl.gov.in/service/idr/"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
HISTORICAL_SOURCES_PATH = PROJECT_ROOT / "ambedkar_archive_data" / "metadata" / "historical_sources.json"
USER_AGENT = "AmbedkarHeritageArchive/1.0 (public catalog metadata; contact archive administrator)"


@dataclass
class FetchStatus:
    source: str
    status: str
    records: list[dict[str, Any]]
    message: str


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[dict[str, str]] = []
        self._href = ""
        self._parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "a":
            self._href = dict(attrs).get("href") or ""
            self._parts = []

    def handle_data(self, data: str) -> None:
        if self._href:
            self._parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self._href:
            label = " ".join(" ".join(self._parts).split())
            self.links.append({"href": self._href, "label": label})
            self._href = ""
            self._parts = []


def _get(url: str, timeout: int = 18) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xml,application/pdf,*/*"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read(8 * 1024 * 1024 + 1)[:8 * 1024 * 1024]


def _stable_id(source: str, url: str) -> str:
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:20].upper()
    return f"DOC_{source.upper()}_CAT_{digest}"


def _record(source: str, title: str, url: str, *, pdf_url: str = "", date: str | None = None, collection: str = "") -> dict[str, Any]:
    clean_title = " ".join(html.unescape(re.sub(r"\s+", " ", title)).split()).strip(" -|•")
    record = {
        "id": _stable_id(source, url),
        "title": clean_title[:500] or "Untitled archive record",
        "author": "Dr. B. R. Ambedkar" if source == "Foundation" else "Constituent Assembly",
        "date": date,
        "type": "publication" if source == "Foundation" else "debate",
        "language": "en",
        "source": source,
        "archive_reference": url,
        "collection": collection,
        "pages": 0,
        "word_count": 0,
        "summary": f"Catalog record from {source}. Open the official repository for its description and available files.",
        "full_text": "",
        "tags": "catalog metadata",
        "translations_json": "{}",
        "media_json": "{}",
        "raw_json": "",
    }
    wrapper = {"document": {
        "id": record["id"], "title": record["title"], "author": record["author"],
        "date": date, "type": record["type"], "language": record["language"],
        "content": {"full_text": "", "summary": record["summary"], "key_quotes": []},
        "metadata": {"source": source, "archive_reference": url, "collection": collection,
                     "pages": 0, "word_count": 0, "url": url, "pdf_url": pdf_url},
        "tags": ["catalog metadata"], "relations": {}, "translations": {}, "media": {}
    }}
    record["raw_json"] = json.dumps(wrapper, ensure_ascii=False)
    return record


def fetch_foundation(limit: int) -> FetchStatus:
    try:
        page = _get(DAF_CATALOG_URL).decode("utf-8", "replace")
        parser = LinkParser()
        parser.feed(page)
        records = []
        seen: set[str] = set()
        for item in parser.links:
            absolute = urllib.parse.urljoin(DAF_CATALOG_URL, item["href"])
            parsed = urllib.parse.urlparse(absolute)
            host = parsed.netloc.lower().removeprefix("www.")
            if host not in {"ambedkarfoundation.nic.in", "drambedkarwritings.gov.in"}:
                continue
            if not (parsed.path.lower().endswith(".pdf") or re.search(r"writings-and-speeches/.*\.php", parsed.path, re.I)):
                continue
            if absolute in seen or not item["label"]:
                continue
            seen.add(absolute)
            title = item["label"]
            # Detail pages often expose the primary PDF; retain only its official link.
            pdf_url = ""
            try:
                detail = _get(absolute, timeout=12).decode("utf-8", "replace")
                detail_parser = LinkParser()
                detail_parser.feed(detail)
                pdf_url = next((urllib.parse.urljoin(absolute, link["href"]) for link in detail_parser.links
                                if urllib.parse.urlparse(urllib.parse.urljoin(absolute, link["href"])).path.lower().endswith(".pdf")), "")
                if not title or len(title) < 5:
                    title = re.sub(r"[-_]+", " ", urllib.parse.urlparse(absolute).path.rsplit("/", 1)[-1].removesuffix(".php"))
            except (OSError, urllib.error.URLError):
                pass
            records.append(_record("Foundation", title, absolute, pdf_url=pdf_url, collection="Writings and Speeches"))
            if pdf_url:
                records[-1]["media_json"] = json.dumps({"official_pdf_url": pdf_url}, ensure_ascii=False)
                wrapper = json.loads(records[-1]["raw_json"])
                wrapper["document"]["media"] = {"official_pdf_url": pdf_url}
                records[-1]["raw_json"] = json.dumps(wrapper, ensure_ascii=False)
            if len(records) >= limit:
                break
        if not records:
            return FetchStatus("Foundation", "unavailable", [], "Official catalog returned no parseable work records.")
        return FetchStatus("Foundation", "ready", records, f"Read {len(records)} public catalog records; full texts were not copied.")
    except (OSError, urllib.error.URLError, UnicodeError) as error:
        return FetchStatus("Foundation", "unavailable", [], f"Could not reach the official catalog: {error}")


def _find_date(text: str) -> str | None:
    match = re.search(r"(?<!\d)(\d{1,2})[-/]([A-Za-z]{3,9}|\d{1,2})[-/](\d{4})(?!\d)", text)
    if not match:
        match = re.search(r"(\d{4})[-/](\d{2})[-/](\d{2})", text)
        if match:
            return f"{match.group(1)}-{match.group(2)}-{match.group(3)}"
        return None
    day, month, year = match.groups()
    months = {name.lower(): f"{index:02}" for index, name in enumerate(("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"), 1)}
    month_number = months.get(month[:3].lower(), month.zfill(2) if month.isdigit() else "01")
    return f"{year}-{month_number}-{day.zfill(2)}"


def fetch_cad(limit: int) -> FetchStatus:
    base_url = os.getenv("CAD_CATALOG_URL", CAD_COLLECTION_URL)
    try:
        page = _get(base_url).decode("utf-8", "replace")
        parser = LinkParser()
        parser.feed(page)
        records = []
        seen: set[str] = set()
        for item in parser.links:
            absolute = urllib.parse.urljoin(base_url, item["href"])
            path = urllib.parse.urlparse(absolute).path
            if "eparlib.sansad.in" not in urllib.parse.urlparse(absolute).netloc or not re.search(r"/handle/\d+/\d+", path):
                continue
            if absolute in seen or len(item["label"]) < 5:
                continue
            seen.add(absolute)
            label = item["label"]
            # DSpace pages may expose parent and navigation links; keep date-like debate records.
            date = _find_date(label)
            if not date and not re.search(r"debate|assembly|constitution|volume|vol\.?\s*\d", label, re.I):
                continue
            records.append(_record("CAD", label, absolute, date=date, collection="Constituent Assembly Debates"))
            if len(records) >= limit:
                break
        if not records:
            return FetchStatus("CAD", "unavailable", [], "Official collection returned no parseable item records.")
        return FetchStatus("CAD", "ready", records, f"Read {len(records)} public debate catalog records; source files remain at Parliament Digital Library.")
    except (OSError, urllib.error.URLError, UnicodeError) as error:
        return FetchStatus("CAD", "unavailable", [], f"Could not reach the official catalog: {error}")


def fetch_ndli(limit: int) -> FetchStatus:
    endpoint = os.getenv("NDLI_OAI_ENDPOINT", "").strip()
    if not endpoint:
        return FetchStatus("NDL", "requires_institutional_access", [],
                           f"No authorized NDLI/partner OAI-PMH endpoint configured. See {NDLI_INFO_URL}; NDLI describes institutional readiness and MoU steps before harvesting.")
    params = urllib.parse.urlencode({"verb": "ListRecords", "metadataPrefix": "oai_dc"})
    url = endpoint + ("&" if "?" in endpoint else "?") + params
    try:
        root = ET.fromstring(_get(url, timeout=25))
        ns = {"oai": "http://www.openarchives.org/OAI/2.0/", "dc": "http://purl.org/dc/elements/1.1/"}
        records = []
        for item in root.findall(".//oai:record", ns):
            header = item.find("oai:header", ns)
            if header is not None and header.attrib.get("status") == "deleted":
                continue
            metadata = item.find("oai:metadata", ns)
            if metadata is None:
                continue
            title_node = metadata.find(".//dc:title", ns)
            identifier_node = metadata.find(".//dc:identifier", ns)
            title = (title_node.text or "").strip() if title_node is not None else ""
            identifier = (identifier_node.text or "").strip() if identifier_node is not None else ""
            if not title or not identifier.startswith(("https://", "http://")):
                continue
            searchable_metadata = " ".join(node.text or "" for node in metadata.findall(".//dc:subject", ns) + metadata.findall(".//dc:description", ns))
            if not re.search(r"ambedkar|आंबेडकर|आंबेडकर|bhimrao|babasaheb", f"{title} {searchable_metadata}", re.I):
                continue
            language_node = metadata.find(".//dc:language", ns)
            language = (language_node.text or "en").strip().lower()[:2] if language_node is not None else "en"
            record = _record("NDL", title, identifier, collection="National Digital Library of India")
            record["language"] = language if re.fullmatch(r"[a-z]{2}", language) else "en"
            wrapper = json.loads(record["raw_json"])
            wrapper["document"]["language"] = record["language"]
            record["raw_json"] = json.dumps(wrapper, ensure_ascii=False)
            records.append(record)
            if len(records) >= limit:
                break
        if not records:
            return FetchStatus("NDL", "empty", [], "Authorized endpoint responded, but no usable public metadata records were returned.")
        return FetchStatus("NDL", "ready", records, f"Read {len(records)} metadata records from the configured authorized endpoint.")
    except (OSError, urllib.error.URLError, ET.ParseError) as error:
        return FetchStatus("NDL", "unavailable", [], f"Configured NDLI endpoint could not be harvested: {error}")


def fetch_sources(limit: int = 100) -> list[FetchStatus]:
    safe_limit = max(1, min(int(limit), 500))
    statuses = [fetch_foundation(safe_limit), fetch_cad(safe_limit), fetch_ndli(safe_limit)]
    try:
        curated = json.loads(HISTORICAL_SOURCES_PATH.read_text(encoding="utf-8"))
        for item in curated:
            source = item["source"]
            url = item["url"]
            record = _record(source, item["title"], url, date=item.get("date"), collection=item.get("collection", ""))
            record.update({
                "id": item["id"],
                "author": item.get("author", record["author"]),
                "type": item.get("type", record["type"]),
                "language": item.get("language", "en"),
                "summary": item["summary"],
                "tags": ", ".join(item.get("tags", ["historical source"])),
                "archive_reference": url,
            })
            wrapper = {"document": {
                "id": record["id"], "title": record["title"], "author": record["author"],
                "date": record["date"], "type": record["type"], "language": record["language"],
                "content": {"full_text": "", "summary": record["summary"], "key_quotes": []},
                "metadata": {"source": source, "archive_reference": url, "collection": record["collection"],
                             "pages": 0, "word_count": 0, "url": url, "pdf_url": url if url.lower().endswith(".pdf") else ""},
                "tags": item.get("tags", ["historical source"]), "relations": {}, "translations": {}, "media": {}
            }}
            record["raw_json"] = json.dumps(wrapper, ensure_ascii=False)
            target = next((status for status in statuses if status.source == source), None)
            if target:
                if not any(existing["id"] == record["id"] for existing in target.records):
                    target.records.append(record)
                    target.message += f" Includes curated historical reference: {record['title']}."
                    if target.status == "unavailable":
                        target.status = "partial"
                    if target.status == "unavailable":
                        target.status = "partial"
            else:
                statuses.append(FetchStatus(source, "ready", [record], "Curated historical catalog reference."))
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as error:
        statuses.append(FetchStatus("Historical", "unavailable", [], f"Could not load curated historical references: {error}"))
    return statuses
