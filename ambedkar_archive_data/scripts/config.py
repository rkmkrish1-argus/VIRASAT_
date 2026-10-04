import os
from pathlib import Path

# Base Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BASE_DIR = PROJECT_ROOT
RAW_DOCS_DIR = BASE_DIR / "raw_documents"
PROCESSED_DATA_DIR = BASE_DIR / "processed_data"
METADATA_DIR = BASE_DIR / "metadata"
IMAGES_DIR = BASE_DIR / "images"
AUDIO_VIDEO_DIR = BASE_DIR / "audio_video"
TEXTS_DIR = BASE_DIR / "texts"
DATABASE_DIR = BASE_DIR / "database"
SCRIPTS_DIR = BASE_DIR / "scripts"

# Output Files
REGISTRY_JSON_PATH = METADATA_DIR / "registry.json"
COMBINED_METADATA_CSV_PATH = METADATA_DIR / "combined_metadata.csv"
DATA_INVENTORY_REPORT_PATH = METADATA_DIR / "data_inventory_report.json"
SQLITE_DB_PATH = DATABASE_DIR / "ambedkar_archive.db"

# Schema Constants
SUPPORTED_LANGUAGES = [
    "en", "hi", "mr", "ta", "te", "ka", "bn", "gu", "pa", "ml"
]

SUPPORTED_TYPES = [
    "speech", "manuscript", "debate", "publication", "letter", "other"
]

SUPPORTED_SOURCES = [
    "IA", "CAD", "Foundation", "NDL", "Columbia"
]

def init_directories():
    """Ensure all archive directory paths exist."""
    dirs = [
        BASE_DIR,
        RAW_DOCS_DIR,
        PROCESSED_DATA_DIR,
        METADATA_DIR,
        IMAGES_DIR,
        AUDIO_VIDEO_DIR,
        TEXTS_DIR,
        DATABASE_DIR,
        SCRIPTS_DIR
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
    return True
