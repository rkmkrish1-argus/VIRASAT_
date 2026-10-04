"""
Schema Normalizer & Enrichment Engine
Converts heterogeneous raw data from Internet Archive, CAD, and Foundation into
the standardized Part 7 JSON Schema.
"""

import re
import hashlib
import logging
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Standard tag taxonomy
TAG_KEYWORDS = {
    "constitutional": ["constitution", "constituent", "assembly", "draft", "article", "amendment", "law", "jurisprudence"],
    "social_justice": ["social", "justice", "untouchable", "depressed", "backward", "dalit", "emancipation"],
    "equality": ["equality", "fraternity", "liberty", "equal", "discrimination"],
    "rights": ["fundamental rights", "human rights", "civil liberties", "safeguards"],
    "caste": ["caste", "varna", "shudra", "brahmin", "jat-pat", "endogamy"],
    "dalits": ["dalit", "scheduled caste", "mahar", "depressed classes"],
    "economics": ["rupee", "currency", "gold", "banking", "finance", "economy", "taxation"],
    "labor": ["labour", "labor", "worker", "wages", "trade union", "strike"],
    "democracy": ["democracy", "parliament", "vote", "election", "executive", "legislative"],
    "buddhism": ["buddha", "dhamma", "sangha", "morality", "conversion", "diksha"]
}

def auto_detect_tags(text: str, default_tags: List[str] = None) -> List[str]:
    """Detect tags by scanning text against key concepts."""
    found = set(default_tags or [])
    lowered = text.lower()
    for tag, keywords in TAG_KEYWORDS.items():
        for kw in keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', lowered):
                found.add(tag)
                break
    if not found:
        found.add("social_justice")
    return sorted(list(found))

def make_doc_id(prefix: str, identifier: str) -> str:
    """Create a clean unique ID for the document."""
    clean_id = re.sub(r'[^a-zA-Z0-9_-]', '_', identifier)
    if len(clean_id) > 40:
        h = hashlib.md5(identifier.encode('utf-8')).hexdigest()[:8]
        clean_id = f"{clean_id[:30]}_{h}"
    return f"{prefix}_{clean_id}"

def normalize_ia_record(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Transform an Internet Archive item into the Part 7 Document Schema."""
    raw_id = raw.get("identifier", "unknown")
    doc_id = make_doc_id("DOC_IA", raw_id)
    title = raw.get("title", "Dr. B.R. Ambedkar Archival Document")
    author = raw.get("author", "Dr. B.R. Ambedkar")
    date = raw.get("date", "1950-01-26")
    doc_type = raw.get("type", "publication")
    lang = raw.get("language", "en")
    desc = raw.get("description", "")
    downloads = raw.get("downloads", 0)

    # Estimate pages and words
    text_content = desc if desc else f"Digital archival manuscript held in Internet Archive repository under identifier {raw_id}. Published works and reference materials associated with Dr. B.R. Ambedkar."
    words = len(text_content.split())
    pages = max(1, words // 300)

    # Summary and quotes
    summary = desc[:280] + "..." if len(desc) > 280 else (desc or f"Archival publication preserved in digital repository: {title}")
    quotes = [
        f"Archival record preserved: {title}",
        "Educate, Agitate, Organize - Dr. B.R. Ambedkar"
    ]

    tags = auto_detect_tags(f"{title} {desc}")

    # Standard Part 7 schema structure
    doc = {
        "document": {
            "id": doc_id,
            "title": title,
            "author": author,
            "date": date,
            "type": doc_type,
            "language": lang,
            "content": {
                "full_text": text_content,
                "summary": summary,
                "key_quotes": quotes
            },
            "metadata": {
                "source": "IA",
                "archive_reference": raw_id,
                "collection": "Internet Archive Ambedkar Collection",
                "pages": pages,
                "word_count": words,
                "condition": "good",
                "accessibility": "public",
                "downloads": downloads,
                "url": raw.get("url"),
                "pdf_url": raw.get("pdf_url")
            },
            "tags": tags,
            "relations": {
                "references": [],
                "related_to": ["DOC_CAD_CAD_VOL11_19491125"],
                "debates": []
            },
            "translations": {
                "hi": {
                    "title": f"{title} (अभिलेखागार प्रति)",
                    "summary": f"डॉ. बी.आर. अंबेडकर अभिलेखागार डिजिटल संग्रह: {title}",
                    "text_url": raw.get("url")
                },
                "mr": {
                    "title": f"{title} (डिजिटल संग्रह प्रत)",
                    "summary": f"डॉ. बाबासाहेब आंबेडकर डिजिटल अभिलेखागार संग्रह: {title}",
                    "text_url": raw.get("url")
                }
            },
            "media": {
                "images": [],
                "audio": raw.get("url") if raw.get("mediatype") == "audio" else None,
                "video": raw.get("url") if raw.get("mediatype") in ["movies", "video"] else None
            }
        }
    }
    return doc

def normalize_cad_record(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Transform a Constituent Assembly Debate item into the Part 7 Document Schema."""
    raw_id = raw.get("debate_id", "unknown")
    doc_id = f"DOC_CAD_{raw_id}"
    title = f"Constituent Assembly Debates: {raw.get('title')}"
    author = "Dr. B.R. Ambedkar"
    date = raw.get("date", "1948-11-04")
    volume = raw.get("volume", "Volume VII")
    page = raw.get("page", "1-50")
    full_text = raw.get("full_text", "")
    summary = raw.get("summary", "")
    quotes = raw.get("key_quotes", [])
    tags = auto_detect_tags(f"{title} {full_text} {raw.get('topic', '')}", raw.get("tags", []))
    words = len(full_text.split())

    doc = {
        "document": {
            "id": doc_id,
            "title": title,
            "author": author,
            "date": date,
            "type": "debate",
            "language": "en",
            "content": {
                "full_text": full_text,
                "summary": summary,
                "key_quotes": quotes
            },
            "metadata": {
                "source": "CAD",
                "archive_reference": f"CAD-LS-{volume}-{page}",
                "collection": f"Constituent Assembly of India Debates ({volume})",
                "pages": 12,
                "word_count": words,
                "condition": "good",
                "accessibility": "public",
                "volume": volume,
                "page_reference": page,
                "speaker_role": "Chairman, Drafting Committee"
            },
            "tags": tags,
            "relations": {
                "references": ["BAWS_PUB_1936_AOC", "BAWS_PUB_1947_SAM"],
                "related_to": ["DOC_CAD_CAD_VOL07_19481104", "DOC_CAD_CAD_VOL11_19491125"],
                "debates": [raw_id]
            },
            "translations": {
                "hi": {
                    "title": f"संविधान सभा वाद-विवाद: {raw.get('title')}",
                    "summary": f"डॉ. बी.आर. अंबेडकर द्वारा संविधान सभा में वक्तव्य: {summary}",
                    "text_url": f"https://www.loksabha.gov.in/DisplayCAD"
                },
                "mr": {
                    "title": f"घटना समिती वादविवाद: {raw.get('title')}",
                    "summary": f"डॉ. बाबासाहेब आंबेडकरांचे घटना समितीमधील ऐतिहासिक भाषण: {summary}",
                    "text_url": f"https://www.loksabha.gov.in/DisplayCAD"
                }
            },
            "media": {
                "images": ["https://upload.wikimedia.org/wikipedia/commons/c/c3/Dr._B._R._Ambedkar_delivering_a_speech_to_the_Constituent_Assembly.jpg"],
                "audio": None,
                "video": None
            }
        }
    }
    return doc

def normalize_foundation_record(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Transform a Foundation/BAWS treatise into the Part 7 Document Schema."""
    raw_id = raw.get("work_id", "unknown")
    doc_id = f"DOC_DAF_{raw_id}"
    title = raw.get("title", "")
    author = "Dr. B.R. Ambedkar"
    date = raw.get("date", "1936-01-01")
    doc_type = raw.get("type", "publication")
    full_text = raw.get("full_text", "")
    summary = raw.get("summary", "")
    quotes = raw.get("key_quotes", [])
    volume = raw.get("volume", "Dr. Ambedkar Foundation Collection")
    page = raw.get("pages", "1-100")
    tags = auto_detect_tags(f"{title} {full_text}", raw.get("tags", []))
    words = len(full_text.split())

    translations = raw.get("translations", {
        "hi": {
            "title": f"{title} (डॉ. अंबेडकर प्रतिष्ठान)",
            "summary": summary
        },
        "mr": {
            "title": f"{title} (डॉ. आंबेडकर प्रतिष्ठान संग्रह)",
            "summary": summary
        }
    })

    doc = {
        "document": {
            "id": doc_id,
            "title": title,
            "author": author,
            "date": date,
            "type": doc_type,
            "language": "en",
            "content": {
                "full_text": full_text,
                "summary": summary,
                "key_quotes": quotes
            },
            "metadata": {
                "source": "Foundation",
                "archive_reference": f"DAF-{raw_id}",
                "collection": f"Dr. Babasaheb Ambedkar Writings and Speeches ({volume})",
                "pages": 45,
                "word_count": words,
                "condition": "good",
                "accessibility": "public",
                "volume": volume,
                "page_reference": page
            },
            "tags": tags,
            "relations": {
                "references": [],
                "related_to": ["DOC_CAD_CAD_VOL11_19491125"],
                "debates": ["CAD_VOL07_19481104"]
            },
            "translations": translations,
            "media": {
                "images": ["https://upload.wikimedia.org/wikipedia/commons/d/d4/Dr._B._R._Ambedkar.jpg"],
                "audio": None,
                "video": None
            }
        }
    }
    return doc
