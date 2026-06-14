import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def format_chat_response(answer, retrieved_chunks, is_refusal=False, error_educational_url=None):
    """
    Assembles the final structured API response.
    """
    disclaimer = "Facts-only. No investment advice."
    
    # 1. Handle Refusal Payload
    if is_refusal:
        # Default citation link for refusals goes to AMFI educational resources
        citation_url = error_educational_url if error_educational_url else "https://www.amfiindia.com/investor-corner/educational-material.html"
        last_updated = datetime.now().strftime("%Y-%m-%d")
        
        return {
            "answer": answer,
            "citation_url": citation_url,
            "last_updated": last_updated,
            "is_refusal": True,
            "disclaimer": disclaimer
        }

    # 2. Extract Citation details from chunks metadata
    citation_url = "https://www.amfiindia.com/investor-corner/educational-material.html"
    last_updated = datetime.now().strftime("%Y-%m-%d") # Fallback to today if chunk date missing
    
    if retrieved_chunks:
        # Get metadata from the top retrieved chunk
        top_meta = retrieved_chunks[0].get("metadata", {})
        citation_url = top_meta.get("source_url", citation_url)
        # Check if last_updated is present in metadata
        last_updated = top_meta.get("last_updated", last_updated)

    return {
        "answer": answer,
        "citation_url": citation_url,
        "last_updated": last_updated,
        "is_refusal": False,
        "disclaimer": disclaimer
    }

if __name__ == "__main__":
    # Test formatter
    test_chunks = [{
        "id": "hdfc-mid-cap-fund-direct-growth#exit_load",
        "text": "[HDFC Mid Cap Fund Direct Growth] Exit Load: 1%",
        "metadata": {
            "source_url": "https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth",
            "last_updated": "2026-06-14"
        }
    }]
    
    # Test factual format
    factual_res = format_chat_response("The exit load is 1% if redeemed within 1 year.", test_chunks)
    print("\n--- Formatted Factual Response ---")
    print(factual_res)
    
    # Test refusal format
    refusal_res = format_chat_response("I cannot provide investment advice.", [], is_refusal=True, error_educational_url="https://www.sebi.gov.in")
    print("\n--- Formatted Refusal Response ---")
    print(refusal_res)
