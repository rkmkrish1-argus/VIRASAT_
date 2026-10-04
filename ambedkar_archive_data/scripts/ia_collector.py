"""
Internet Archive (Archive.org) Data Collector
Harvests Dr. B.R. Ambedkar archival records, publications, and multimedia.
"""

import time
import json
import logging
from typing import List, Dict, Any
import requests

from config import RAW_DOCS_DIR, init_directories

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

SEARCH_URL = "https://archive.org/advancedsearch.php"

QUERIES = [
    'creator:(Ambedkar)',
    'title:(Ambedkar)',
    'subject:(Ambedkar)',
    'collection:(digitallibraryindia) AND Ambedkar',
    'Ambedkar AND Constitution',
    'Ambedkar AND "Castes in India"',
    'Ambedkar AND "Annihilation of Caste"'
]

LANGUAGE_MAP = {
    "eng": "en", "english": "en", "en": "en",
    "hin": "hi", "hindi": "hi", "hi": "hi",
    "mar": "mr", "marathi": "mr", "mr": "mr",
    "tam": "ta", "tamil": "ta", "ta": "ta",
    "tel": "te", "telugu": "te", "te": "te",
    "kan": "ka", "kannada": "ka", "ka": "ka",
    "ben": "bn", "bengali": "bn", "bn": "bn",
    "guj": "gu", "gujarati": "gu", "gu": "gu",
    "pan": "pa", "punjabi": "pa", "pa": "pa",
    "mal": "ml", "malayalam": "ml", "ml": "ml"
}

def fetch_with_retry(url: str, params: Dict[str, Any], max_retries: int = 3) -> Dict[str, Any]:
    """Execute HTTP GET with exponential backoff retry logic."""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=20)
            if response.status_code == 200:
                return response.json()
            logger.warning(f"HTTP {response.status_code} for query: {params.get('q')}, retry {attempt+1}/{max_retries}")
        except Exception as exc:
            logger.warning(f"Network error on attempt {attempt+1}: {exc}")
        time.sleep(2 ** attempt)
    return {}

def normalize_lang(raw_lang: Any) -> str:
    """Normalize raw language string into ISO 639-1 code."""
    if not raw_lang:
        return "en"
    if isinstance(raw_lang, list):
        raw_lang = raw_lang[0] if raw_lang else "en"
    raw_str = str(raw_lang).lower().strip()
    return LANGUAGE_MAP.get(raw_str, "en")

def collect_from_internet_archive(target_count: int = 500) -> List[Dict[str, Any]]:
    """
    Search and collect Dr. Ambedkar archival items from Internet Archive API.
    """
    init_directories()
    unique_items: Dict[str, Dict[str, Any]] = {}
    rows_per_query = 150

    logger.info("Initiating Internet Archive harvesting for Dr. Ambedkar records...")

    for query in QUERIES:
        if len(unique_items) >= target_count:
            break

        logger.info(f"Querying IA: '{query}' (limit {rows_per_query})")
        params = {
            "q": query,
            "fl[]": [
                "identifier",
                "title",
                "creator",
                "date",
                "description",
                "language",
                "mediatype",
                "downloads",
                "item_size",
                "year"
            ],
            "sort[]": "downloads desc",
            "rows": rows_per_query,
            "output": "json"
        }

        data = fetch_with_retry(SEARCH_URL, params)
        docs = data.get("response", {}).get("docs", [])
        logger.info(f"Retrieved {len(docs)} documents for query: {query}")

        for doc in docs:
            identifier = doc.get("identifier")
            if not identifier:
                continue

            # Skip duplicate items
            if identifier in unique_items:
                continue

            title = doc.get("title") or identifier.replace("_", " ").title()
            creator = doc.get("creator") or "Dr. B.R. Ambedkar"
            if isinstance(creator, list):
                creator = ", ".join(creator)

            date = doc.get("date") or doc.get("year") or "1950-01-26"
            if isinstance(date, str) and len(date) >= 10 and date[4] == "-" and date[7] == "-":
                clean_date = date[:10]
            elif isinstance(date, str) and len(date) >= 4 and date[:4].isdigit():
                clean_date = f"{date[:4]}-01-01"
            else:
                clean_date = "1950-01-26"

            description = doc.get("description", "")
            if isinstance(description, list):
                description = " ".join(description)

            lang = normalize_lang(doc.get("language"))
            mediatype = doc.get("mediatype", "texts")

            # Determine doc type
            if mediatype == "audio":
                doc_type = "speech"
            elif mediatype in ["movies", "video"]:
                doc_type = "other"
            elif "speech" in title.lower() or "address" in title.lower():
                doc_type = "speech"
            elif "debate" in title.lower():
                doc_type = "debate"
            elif "letter" in title.lower() or "correspondence" in title.lower():
                doc_type = "letter"
            elif "manuscript" in title.lower():
                doc_type = "manuscript"
            else:
                doc_type = "publication"

            record = {
                "source": "IA",
                "identifier": identifier,
                "title": title,
                "author": creator,
                "date": clean_date,
                "type": doc_type,
                "language": lang,
                "mediatype": mediatype,
                "description": description,
                "url": f"https://archive.org/details/{identifier}",
                "pdf_url": f"https://archive.org/download/{identifier}/{identifier}.pdf",
                "downloads": doc.get("downloads", 0)
            }

            unique_items[identifier] = record

    results = list(unique_items.values())
    logger.info(f"Total unique Internet Archive items harvested: {len(results)}")

    # Save to raw documents
    output_file = RAW_DOCS_DIR / "ia_raw_records.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    logger.info(f"Saved raw IA dataset to {output_file}")

    return results

if __name__ == "__main__":
    items = collect_from_internet_archive(550)
    print(f"Acquisition complete: {len(items)} items acquired from Internet Archive.")
