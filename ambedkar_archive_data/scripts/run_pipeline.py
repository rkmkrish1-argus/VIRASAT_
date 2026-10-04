"""
Master Orchestrator: Dr. B.R. Ambedkar Digital Heritage Archive Pipeline
Executes end-to-end data acquisition, schema normalization, validation, and ingestion.
"""

import sys
import time
import logging
from pathlib import Path

# Add scripts directory to module path
scripts_path = Path(__file__).resolve().parent
if str(scripts_path) not in sys.path:
    sys.path.insert(0, str(scripts_path))

from config import init_directories
from ia_collector import collect_from_internet_archive
from cad_collector import collect_cad_speeches
from foundation_collector import collect_foundation_works
from normalizer import normalize_ia_record, normalize_cad_record, normalize_foundation_record
from schema_validator import validate_dataset
from ingest import ingest_documents

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("PipelineOrchestrator")

def execute_pipeline(ia_target_count: int = 500):
    start_time = time.time()
    logger.info("=" * 65)
    logger.info("  DR. B.R. AMBEDKAR DIGITAL HERITAGE ARCHIVE (PS 26096)")
    logger.info("  DATA ACQUISITION & INGESTION PIPELINE")
    logger.info("=" * 65)

    # Step 1: Ensure directory structure
    logger.info("[Step 1/5] Initializing Archive Directories...")
    init_directories()

    # Step 2: Acquire data from open & public repositories
    logger.info("[Step 2/5] Acquiring data from repositories...")
    ia_raw = collect_from_internet_archive(target_count=ia_target_count)
    cad_raw = collect_cad_speeches()
    foundation_raw = collect_foundation_works()

    logger.info(f"Raw data acquired: {len(ia_raw)} IA items, {len(cad_raw)} CAD records, {len(foundation_raw)} Foundation works.")

    # Step 3: Normalize to Unified Schema (Part 7 of Guide)
    logger.info("[Step 3/5] Normalizing into Part 7 Schema...")
    normalized_docs = []

    for raw in ia_raw:
        normalized_docs.append(normalize_ia_record(raw))

    for raw in cad_raw:
        normalized_docs.append(normalize_cad_record(raw))

    for raw in foundation_raw:
        normalized_docs.append(normalize_foundation_record(raw))

    logger.info(f"Total normalized documents prepared: {len(normalized_docs)}")

    # Step 4: Validate Dataset
    logger.info("[Step 4/5] Running Schema & Encoding Validation...")
    val_report = validate_dataset(normalized_docs)
    logger.info(f"Validation Result: Valid={val_report['valid_documents']}, Invalid={val_report['invalid_documents']}")
    if not val_report["is_all_valid"]:
        logger.error(f"Sample validation errors: {val_report['sample_errors']}")
        raise ValueError("Schema validation failed on some records!")

    # Step 5: Ingestion into DB, FTS5 Index, CSV, and Registry
    logger.info("[Step 5/5] Ingesting into Database, FTS5 Index, and Registries...")
    inventory = ingest_documents(normalized_docs)

    elapsed = time.time() - start_time
    logger.info("=" * 65)
    logger.info("  INGESTION PIPELINE EXECUTION COMPLETED SUCCESSFULLY!")
    logger.info("=" * 65)
    logger.info(f"Total Documents Ingested: {inventory['total_documents']}")
    logger.info(f"Total Words Indexed:      {inventory['total_words_indexed']:,}")
    logger.info(f"Embedding Chunks Created: {inventory['total_embedding_chunks']}")
    logger.info(f"Sources Breakdown:        {inventory['breakdown_by_source']}")
    logger.info(f"Languages Breakdown:      {inventory['breakdown_by_language']}")
    logger.info(f"Types Breakdown:          {inventory['breakdown_by_type']}")
    logger.info(f"Database Location:        {inventory['sqlite_db']['path']}")
    logger.info(f"Execution Elapsed Time:   {elapsed:.2f} seconds")
    logger.info("=" * 65)

    return inventory

if __name__ == "__main__":
    execute_pipeline()
