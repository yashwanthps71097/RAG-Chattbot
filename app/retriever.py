import os
import json
import pickle
import logging
import requests
import numpy as np
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

HF_API_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/BAAI/bge-small-en-v1.5"
INDEX_DIR = "data/index"

# Map keywords to scheme slugs defined in corpus.yaml
SCHEME_KEYWORDS = {
    "mid": "hdfc-mid-cap-fund-direct-growth",
    "midcap": "hdfc-mid-cap-fund-direct-growth",
    "large": "hdfc-large-cap-fund-direct-growth",
    "largecap": "hdfc-large-cap-fund-direct-growth",
    "small": "hdfc-small-cap-fund-direct-growth",
    "smallcap": "hdfc-small-cap-fund-direct-growth",
    "gold": "hdfc-gold-etf-fund-of-fund-direct-plan-growth",
    "etf": "hdfc-gold-etf-fund-of-fund-direct-plan-growth",
    "defence": "hdfc-defence-fund-direct-growth",
    "defense": "hdfc-defence-fund-direct-growth"
}

def resolve_scheme_slug(query):
    query_lower = query.lower()
    for kw, slug in SCHEME_KEYWORDS.items():
        if kw in query_lower:
            logging.info(f"Resolved scheme slug '{slug}' for query: '{query}'")
            return slug
    logging.info("No specific scheme resolved in the query. Searching across all schemes.")
    return None

def query_bge_embeddings(text, token=None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    response = requests.post(
        HF_API_URL,
        headers=headers,
        json={"inputs": [text], "options": {"wait_for_model": True}},
        timeout=15
    )
    if response.status_code == 200:
        return response.json()[0]
    else:
        raise Exception(f"Failed to generate query embedding: {response.text}")

def retrieve_from_chromadb(query_text, resolved_slug, token=None):
    import chromadb
    client = chromadb.PersistentClient(path=os.path.join(INDEX_DIR, "chroma"))
    collection = client.get_collection(name="hdfc_funds")
    
    # Generate query embedding
    query_emb = query_bge_embeddings(query_text, token)
    
    # Formulate filter
    where_filter = {"slug": resolved_slug} if resolved_slug else None
    
    results = collection.query(
        query_embeddings=[query_emb],
        where=where_filter,
        n_results=2
    )
    
    retrieved_chunks = []
    if results and "documents" in results and results["documents"]:
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        ids = results["ids"][0]
        
        for idx in range(len(documents)):
            retrieved_chunks.append({
                "id": ids[idx],
                "text": documents[idx],
                "metadata": metadatas[idx]
            })
            
    return retrieved_chunks

def retrieve_from_tfidf(query_text, resolved_slug):
    vectorizer_path = os.path.join(INDEX_DIR, "vectorizer.pkl")
    matrix_path = os.path.join(INDEX_DIR, "tfidf_matrix.pkl")
    chunks_path = os.path.join(INDEX_DIR, "chunks.json")
    
    if not (os.path.exists(vectorizer_path) and os.path.exists(matrix_path) and os.path.exists(chunks_path)):
        raise Exception("TF-IDF Index files are missing. Run ingestion first.")
        
    with open(vectorizer_path, "rb") as f:
        vectorizer = pickle.load(f)
    with open(matrix_path, "rb") as f:
        tfidf_matrix = pickle.load(f)
    with open(chunks_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)
        
    # Transform query to TF-IDF vector
    query_vec = vectorizer.transform([query_text])
    
    # Calculate cosine similarity (dot product)
    # tfidf_matrix shape: (num_chunks, num_features)
    # query_vec shape: (1, num_features)
    similarities = np.dot(tfidf_matrix, query_vec.T).toarray().flatten()
    
    # Get scores linked to chunks
    scored_chunks = []
    for idx, score in enumerate(similarities):
        chunk = chunks[idx]
        slug = chunk["metadata"]["slug"]
        
        # Apply metadata filter
        if resolved_slug and slug != resolved_slug:
            continue
            
        scored_chunks.append({
            "id": chunk["id"],
            "text": chunk["text"],
            "metadata": chunk["metadata"],
            "score": float(score)
        })
        
    # Sort by score descending and return top 2
    scored_chunks.sort(key=lambda x: x["score"], reverse=True)
    return scored_chunks[:2]

def retrieve_context(query_text):
    resolved_slug = resolve_scheme_slug(query_text)
    
    # First priority: Check if ChromaDB collection files exist
    chroma_path = os.path.join(INDEX_DIR, "chroma")
    token = os.getenv("HF_API_TOKEN")
    
    if os.path.exists(chroma_path):
        try:
            logging.info("Attempting retrieval from ChromaDB collection...")
            return retrieve_from_chromadb(query_text, resolved_slug, token)
        except Exception as e:
            logging.error(f"ChromaDB retrieval failed: {e}. Falling back to TF-IDF index...")
            
    # Fallback/Default: Retrieve from local TF-IDF index
    try:
        logging.info("Retrieving context using local TF-IDF index...")
        return retrieve_from_tfidf(query_text, resolved_slug)
    except Exception as e:
        logging.error(f"TF-IDF retrieval failed: {e}")
        return []

if __name__ == "__main__":
    # Test query
    test_q = "What is the exit load of HDFC Small Cap Fund?"
    res = retrieve_context(test_q)
    print(json.dumps(res, indent=4))
