import unittest
import sys
import os

# Add the workspace root to sys.path so we can import from 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.retriever import resolve_scheme_slug, retrieve_context

class TestRetrievalEngine(unittest.TestCase):
    def test_scheme_slug_resolution(self):
        self.assertEqual(
            resolve_scheme_slug("What is the exit load of HDFC Small Cap Fund?"),
            "hdfc-small-cap-fund-direct-growth"
        )
        self.assertEqual(
            resolve_scheme_slug("Who manages the HDFC Defence Fund?"),
            "hdfc-defence-fund-direct-growth"
        )
        self.assertEqual(
            resolve_scheme_slug("Show me details for HDFC Mid Cap Direct Growth."),
            "hdfc-mid-cap-fund-direct-growth"
        )
        self.assertEqual(
            resolve_scheme_slug("Check gold etf options."),
            "hdfc-gold-etf-fund-of-fund-direct-plan-growth"
        )

    def test_context_retrieval(self):
        # Retrieve context for a factual query
        query = "What is the exit load of HDFC Small Cap Fund?"
        chunks = retrieve_context(query)
        
        # Ensure we get up to 2 chunks as per requirements
        self.assertLessEqual(len(chunks), 2)
        
        for chunk in chunks:
            self.assertIn("text", chunk)
            self.assertIn("metadata", chunk)
            # Ensure metadata points to the resolved small cap scheme
            self.assertEqual(chunk["metadata"]["slug"], "hdfc-small-cap-fund-direct-growth")

if __name__ == "__main__":
    unittest.main()
