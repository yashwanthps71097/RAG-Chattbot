import re
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# PII Regular Expressions
PAN_PATTERN = re.compile(r"\b[A-Za-z]{5}[0-9]{4}[A-Za-z]{1}\b")
AADHAAR_PATTERN = re.compile(r"\b[2-9]{1}[0-9]{3}[\s-]*[0-9]{4}[\s-]*[0-9]{4}\b")
PHONE_PATTERN = re.compile(r"\b(?:\+91|0)?[6-9]\d{9}\b")

# Keywords for classification
ADVISORY_KEYWORDS = [
    "should i buy", "should i invest", "which is better", "which one is better",
    "recommend", "investment advice", "is it good to buy", "suggest a fund",
    "give me advice", "performance forecast", "expected returns", "guaranteed return",
    "which fund should i", "better return"
]

SCOPE_KEYWORDS = [
    "hdfc", "mid", "small", "large", "gold", "defence", "defense", "etf", "sip", 
    "lumpsum", "expense ratio", "exit load", "benchmark", "manager", "nav", "aum",
    "lock-in", "minimum", "tax", "riskometer"
]

def clean_query(query):
    # Remove extra spaces and punctuation
    return " ".join(query.strip().split())

def contains_pii(query):
    cleaned = clean_query(query)
    # Check PAN
    if PAN_PATTERN.search(cleaned):
        logging.info("PII Block: PAN pattern detected.")
        return True
    # Check Aadhaar
    if AADHAAR_PATTERN.search(cleaned):
        logging.info("PII Block: Aadhaar pattern detected.")
        return True
    # Check Phone Number
    if PHONE_PATTERN.search(cleaned):
        logging.info("PII Block: Phone number pattern detected.")
        return True
    return False

def classify_query(query):
    """
    Classifies the user query.
    Returns:
        tuple: (category, educational_url_or_reason)
        Categories: "factual", "advisory", "pii_block", "out_of_scope"
    """
    # 1. PII Check
    if contains_pii(query):
        return "pii_block", "Sensitive personal information (PII) detected. For security, do not share PAN, Aadhaar, phone, or bank details."

    cleaned_query = query.lower()

    # 2. Advisory Check
    for kw in ADVISORY_KEYWORDS:
        if kw in cleaned_query:
            logging.info(f"Advisory Block: Match on keyword '{kw}'")
            return "advisory", "https://www.amfiindia.com/investor-corner/educational-material.html"

    # 3. Scope Check
    # Check if the query contains at least one relevant keyword
    has_scope_keyword = any(kw in cleaned_query for kw in SCOPE_KEYWORDS)
    if not has_scope_keyword:
        logging.info("Scope Block: Query does not contain mutual fund or scoped scheme keywords.")
        return "out_of_scope", "I am configured to answer factual questions about the 5 scoped HDFC schemes only (expense ratios, exit loads, minimum SIP, benchmarks, and fund managers)."

    return "factual", None

if __name__ == "__main__":
    # Test classifier
    test_queries = [
        "What is the exit load of HDFC Small Cap Fund?",
        "Should I invest in HDFC Mid Cap?",
        "My PAN card number is ABCDE1234F, what is my limit?",
        "Who won the cricket match yesterday?"
    ]

    print("\n--- Classifier Verification ---")
    for q in test_queries:
        cat, detail = classify_query(q)
        print(f"Query: {q}\nResult: Category={cat}, Details={detail}\n")
