import logging
from ingestion.fetch import fetch_html_for_schemes
from ingestion.parse import parse_all_raw_files
from ingestion.chunk import generate_chunks
from ingestion.index import build_index

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_pipeline():
    logging.info("Starting Ingestion Pipeline...")
    
    # 1. Fetch
    logging.info("--- Step 1: Fetching HTML snapshots ---")
    fetch_html_for_schemes()

    # 2. Parse
    logging.info("--- Step 2: Parsing HTML files ---")
    parse_all_raw_files()

    # 3. Chunk
    logging.info("--- Step 3: Chunking parsed details ---")
    generate_chunks()

    # 4. Index
    logging.info("--- Step 4: Generating embeddings & building index ---")
    build_index()

    logging.info("Ingestion Pipeline completed successfully!")

if __name__ == "__main__":
    run_pipeline()
