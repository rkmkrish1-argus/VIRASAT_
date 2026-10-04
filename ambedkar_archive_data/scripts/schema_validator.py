"""
Schema Validation Module
Verifies that all normalized records strictly adhere to the Part 7 JSON specification.
"""

import logging
from typing import Dict, Any, List, Tuple
from config import SUPPORTED_LANGUAGES, SUPPORTED_TYPES, SUPPORTED_SOURCES

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

REQUIRED_ROOT_KEYS = ["document"]
REQUIRED_DOC_KEYS = [
    "id", "title", "author", "date", "type", "language",
    "content", "metadata", "tags", "relations"
]
REQUIRED_CONTENT_KEYS = ["full_text", "summary", "key_quotes"]
REQUIRED_METADATA_KEYS = ["source", "archive_reference", "collection", "condition", "accessibility"]

def validate_document(doc_obj: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate a single document against Part 7 specification."""
    errors = []

    if "document" not in doc_obj:
        return False, ["Missing root 'document' key"]

    doc = doc_obj["document"]

    # Check top-level required fields
    for k in REQUIRED_DOC_KEYS:
        if k not in doc or doc[k] is None:
            errors.append(f"Missing required field: '{k}'")

    # Check doc_type
    doc_type = doc.get("type")
    if doc_type not in SUPPORTED_TYPES:
        errors.append(f"Invalid document type: '{doc_type}' (expected one of {SUPPORTED_TYPES})")

    # Check language
    lang = doc.get("language")
    if lang not in SUPPORTED_LANGUAGES:
        errors.append(f"Unsupported language code: '{lang}'")

    # Check content structure
    content = doc.get("content", {})
    if not isinstance(content, dict):
        errors.append("'content' must be an object")
    else:
        for ck in REQUIRED_CONTENT_KEYS:
            if ck not in content:
                errors.append(f"Missing required content field: '{ck}'")

    # Check metadata structure
    meta = doc.get("metadata", {})
    if not isinstance(meta, dict):
        errors.append("'metadata' must be an object")
    else:
        source = meta.get("source")
        if source not in SUPPORTED_SOURCES:
            errors.append(f"Invalid metadata source: '{source}'")
        for mk in REQUIRED_METADATA_KEYS:
            if mk not in meta:
                errors.append(f"Missing required metadata field: '{mk}'")

    # Check tags
    tags = doc.get("tags")
    if not isinstance(tags, list):
        errors.append("'tags' must be a list of strings")

    return len(errors) == 0, errors

def validate_dataset(documents: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Validate entire dataset and compile validation metrics."""
    valid_count = 0
    invalid_count = 0
    all_errors = []

    for idx, doc in enumerate(documents):
        is_valid, errors = validate_document(doc)
        if is_valid:
            valid_count += 1
        else:
            invalid_count += 1
            doc_id = doc.get("document", {}).get("id", f"index_{idx}")
            all_errors.append({"doc_id": doc_id, "errors": errors})

    report = {
        "total_documents": len(documents),
        "valid_documents": valid_count,
        "invalid_documents": invalid_count,
        "is_all_valid": invalid_count == 0,
        "sample_errors": all_errors[:10]
    }
    return report
