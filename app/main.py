import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional

from app.classifier import classify_query
from app.retriever import retrieve_context
from app.generator import generate_answer
from app.validator import is_grounded_and_compliant
from app.formatter import format_chat_response

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI(title="Mutual Fund FAQ Assistant")

# CORS setup for React frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    query = request.message.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query message cannot be empty.")

    logging.info(f"Received query: '{query}'")

    try:
        # 1. Classify the query
        category, details = classify_query(query)
        logging.info(f"Query classified as: category={category}, details={details}")

        if category == "pii_block":
            # Return refusal with custom PII warning
            return format_chat_response(
                answer=details,
                retrieved_chunks=[],
                is_refusal=True
            )

        elif category in ("advisory", "out_of_scope"):
            # Return refusal with official educational URL or category explanation
            refusal_msg = (
                "I can only answer factual questions about the 5 scoped HDFC schemes in my corpus "
                "(such as expense ratios, exit loads, minimum SIP, benchmarks, and fund manager details). "
                "I cannot provide investment advice or compare funds."
            )
            if category == "out_of_scope" and details:
                refusal_msg = details

            return format_chat_response(
                answer=refusal_msg,
                retrieved_chunks=[],
                is_refusal=True,
                error_educational_url=details if category == "advisory" else None
            )

        # 2. Retrieval Stage
        retrieved_chunks = retrieve_context(query)
        logging.info(f"Retrieved {len(retrieved_chunks)} context chunks.")

        if not retrieved_chunks:
            # Fallback if no matching chunks found
            fallback_msg = "I cannot find verified details in the official documents for this question."
            return format_chat_response(
                answer=fallback_msg,
                retrieved_chunks=[],
                is_refusal=True
            )

        # 3. LLM Generation Stage
        answer = generate_answer(query, retrieved_chunks)
        logging.info(f"Generated answer: {answer}")

        # 4. Post-Generation Validation Stage
        is_valid, validation_err = is_grounded_and_compliant(answer, retrieved_chunks)
        if not is_valid:
            logging.warning(f"Validation failed: {validation_err}. Serving safe fallback refusal.")
            fallback_msg = "I cannot find verified details in the official documents for this question."
            return format_chat_response(
                answer=fallback_msg,
                retrieved_chunks=retrieved_chunks,
                is_refusal=True
            )

        # 5. Format Successful Response
        formatted_response = format_chat_response(
            answer=answer,
            retrieved_chunks=retrieved_chunks,
            is_refusal=False
        )
        # Append source chunks text for frontend verification popup
        formatted_response["source_chunks"] = [chunk["text"] for chunk in retrieved_chunks if "text" in chunk]
        return formatted_response

    except Exception as e:
        logging.error(f"Error processing chat request: {e}", exc_info=True)
        # Safe fallback server error response
        return format_chat_response(
            answer="An internal server error occurred while processing your request. Please try again later.",
            retrieved_chunks=[],
            is_refusal=True
        )

# Mount frontend production build directory (if exists)
ui_dist_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ui", "dist"))
if os.path.exists(ui_dist_path):
    logging.info(f"Mounting frontend static files from: {ui_dist_path}")
    app.mount("/", StaticFiles(directory=ui_dist_path, html=True), name="ui")
else:
    logging.warning(f"Frontend build folder '{ui_dist_path}' not found. Serving API endpoints only.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
