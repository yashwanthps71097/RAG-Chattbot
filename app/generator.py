import os
import logging
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize the Groq Client
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key_here":
    logging.warning("GROQ_API_KEY is not configured or contains the default placeholder.")

client = Groq(api_key=GROQ_API_KEY)

def generate_answer(user_query, retrieved_chunks):
    # If no chunks are retrieved, return a default out-of-scope response
    if not retrieved_chunks:
        return "I cannot find verified details in the official documents for this question."

    # 1. Format the retrieved context chunks
    context_text = ""
    for chunk in retrieved_chunks:
        context_text += f"Fact segment (Source: {chunk['metadata']['source_url']}):\n{chunk['text']}\n\n"

    # 2. Build the strict Facts-Only System Prompt
    system_prompt = f"""You are a facts-only Mutual Fund Assistant. 
Your goal is to answer the user's question using ONLY the verified facts context provided below.

Strict Constraints:
1. Do NOT provide any investment advice, opinions, suggestions, or recommendations (e.g., do not say "this is a good option" or "should invest").
2. Answer based strictly on the facts provided in the Context. If the context does not contain the answer, politely refuse and state: "I cannot find verified details in the official documents for this question."
3. Do NOT make comparisons between schemes unless both are in the context.
4. Limit your response to a maximum of 3 sentences.
5. Do NOT include any URLs or citation links within the text body of your response.

Context Facts:
{context_text}"""

    try:
        # 3. Call Groq API
        logging.info("Requesting completion from Groq API...")
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            model="llama-3.1-8b-instant",
            temperature=0.0,  # Strict grounding, no creativity
            max_tokens=150
        )
        
        answer = chat_completion.choices[0].message.content
        return answer.strip()
        
    except Exception as e:
        logging.error(f"Error querying Groq API: {e}")
        return f"Error: Failed to generate response due to API connection error."

if __name__ == "__main__":
    from app.retriever import retrieve_context
    import json

    # Test query to check if the Groq API connection is working
    test_query = "What is the exit load of HDFC Small Cap Fund?"
    logging.info(f"Running End-to-End Integration Test for Query: '{test_query}'")
    
    # Get retrieved context chunks
    chunks = retrieve_context(test_query)
    logging.info(f"Retrieved {len(chunks)} context chunks.")
    
    # Generate the grounded answer
    answer = generate_answer(test_query, chunks)
    
    print("\n--- Test Verification Result ---")
    print(f"Query: {test_query}")
    print(f"Response: {answer}")
    print("---------------------------------")
