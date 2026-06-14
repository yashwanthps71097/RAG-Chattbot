import unittest
import sys
import os

# Add the workspace root to sys.path so we can import from 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.classifier import classify_query

class TestQueryClassifier(unittest.TestCase):
    def test_factual_queries(self):
        factual_cases = [
            "What is the exit load of HDFC Small Cap Fund?",
            "Who manages HDFC Defence Fund?",
            "Show me the expense ratio of HDFC Mid Cap Fund.",
            "What is the benchmark index for HDFC Gold ETF?",
            "What is the minimum SIP for HDFC Large Cap Fund?"
        ]
        for query in factual_cases:
            category, _ = classify_query(query)
            self.assertEqual(category, "factual", f"Failed for query: {query}")

    def test_advisory_queries(self):
        advisory_cases = [
            "Should I invest in HDFC Mid Cap?",
            "Which is better, HDFC Small Cap or HDFC Mid Cap?",
            "Please recommend a good HDFC mutual fund.",
            "Suggest a fund for high returns.",
            "Is it good to buy HDFC top 100?"
        ]
        for query in advisory_cases:
            category, detail = classify_query(query)
            self.assertEqual(category, "advisory", f"Failed for query: {query}")
            self.assertIsNotNone(detail)

    def test_pii_blocking(self):
        pii_cases = [
            "My PAN number is ABCDE1234F",
            "Contact me at +91 9876543210 for details",
            "Here is my Aadhaar card: 9234-5678-9012"
        ]
        for query in pii_cases:
            category, detail = classify_query(query)
            self.assertEqual(category, "pii_block", f"Failed for query: {query}")
            self.assertIn("personal information", detail.lower())

    def test_out_of_scope(self):
        out_of_scope_cases = [
            "Who won the cricket match yesterday?",
            "What is the weather in Delhi?",
            "Explain how a steam engine works.",
            "How to cook paneer butter masala?"
        ]
        for query in out_of_scope_cases:
            category, detail = classify_query(query)
            self.assertEqual(category, "out_of_scope", f"Failed for query: {query}")
            self.assertIsNotNone(detail)

if __name__ == "__main__":
    unittest.main()
