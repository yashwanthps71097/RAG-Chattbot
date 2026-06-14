import os
import json
import logging
import requests
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

HF_API_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/BAAI/bge-small-en-v1.5"

def query_embeddings(texts, token=None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
        
    logging.info("Requesting embeddings from Hugging Face Inference API for BGE-small...")
    response = requests.post(
        HF_API_URL,
        headers=headers,
        json={"inputs": texts, "options": {"wait_for_model": True}},
        timeout=30
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to generate embeddings. Status Code: {response.status_code}, Error: {response.text}")

def build_index(chunks_path="data/processed/chunks.json", index_dir="data/index"):
    os.makedirs(index_dir, exist_ok=True)

    if not os.path.exists(chunks_path):
        logging.error(f"Chunks file {chunks_path} does not exist. Run chunker first.")
        return

    with open(chunks_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    texts = [chunk["text"] for chunk in chunks]
    ids = [chunk["id"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]
    token = os.getenv("HF_API_TOKEN")

    try:
        # 1. Compute BGE-small embeddings via API
        embeddings = query_embeddings(texts, token)
        
        if len(embeddings) != len(chunks):
            raise Exception("Dimension mismatch between computed embeddings and source chunks.")

        # 2. Try to initialize and save to ChromaDB
        try:
            import chromadb
            logging.info("Initializing ChromaDB persistent store...")
            client = chromadb.PersistentClient(path=os.path.join(index_dir, "chroma"))
            
            # Reset/Create collection
            try:
                client.delete_collection("hdfc_funds")
            except Exception:
                pass
                
            collection = client.create_collection(name="hdfc_funds")
            
            logging.info("Adding documents and vectors to ChromaDB...")
            collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas
            )
            logging.info("Successfully loaded index into local ChromaDB store.")
            
        except ImportError:
            logging.warning("ChromaDB library is not installed. Saving embeddings in a flat file index instead...")
            # Fallback to local flat JSON vector index
            indexed_data = []
            for chunk, embedding in zip(chunks, embeddings):
                indexed_chunk = chunk.copy()
                indexed_chunk["embedding"] = embedding
                indexed_data.append(indexed_chunk)

            with open(os.path.join(index_dir, "index.json"), "w", encoding="utf-8") as f:
                json.dump(indexed_data, f, indent=4)
            logging.info("Successfully saved flat vector index to data/index/index.json.")
            
    except Exception as e:
        logging.error(f"Error building BGE-small index: {e}")
        # Fallback to TF-IDF
        logging.warning("Falling back to local TF-IDF vector index build...")
        from sklearn.feature_extraction.text import TfidfVectorizer
        import pickle
        
        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        tfidf_matrix = vectorizer.fit_transform(texts)

        with open(os.path.join(index_dir, "vectorizer.pkl"), "wb") as f:
            pickle.dump(vectorizer, f)
        with open(os.path.join(index_dir, "tfidf_matrix.pkl"), "wb") as f:
            pickle.dump(tfidf_matrix, f)
        with open(os.path.join(index_dir, "chunks.json"), "w", encoding="utf-8") as f:
            json.dump(chunks, f, indent=4)
            
        logging.info("TF-IDF fallback index successfully created.")

if __name__ == "__main__":
    build_index()
