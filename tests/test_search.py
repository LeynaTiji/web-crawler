import unittest
from io import StringIO
import sys

from src.search import find_query, print_word

SAMPLE_INDEX = {
    "good": {
        "https://example.com/page1": {"freq": 3, "positions": [0, 5, 12]},
        "https://example.com/page2": {"freq": 1, "positions": [4]},
    },
    "friends": {
        "https://example.com/page1": {"freq": 2, "positions": [1, 8]},
    },
    "morning": {
        "https://example.com/page2": {"freq": 1, "positions": [0]},
    },
}


class TestFind(unittest.TestCase):

    def test_single_word_returns_matching_pages(self):
        results = find_query("good", SAMPLE_INDEX)
        urls = [url for url, _ in results]
        self.assertIn("https://example.com/page1", urls)
        self.assertIn("https://example.com/page2", urls)
 
    def test_single_word_not_in_index_returns_empty(self):
        results = find_query("interesting", SAMPLE_INDEX)
        self.assertEqual(results, [])

    def test_multi_word(self):
        results = find_query("good friends", SAMPLE_INDEX)
        urls = [url for url, _ in results]
        self.assertEqual(urls, ["https://example.com/page1"])

    def test_multi_word_with_no_common_pages(self):
        results = find_query("morning friends", SAMPLE_INDEX)
        self.assertEqual(results, [])

    def test_empty_query_returns_empty(self):
        results = find_query("", SAMPLE_INDEX)
        self.assertEqual(results, [])

    def test_case_insensitive(self):
        results_lower = find_query("good", SAMPLE_INDEX)
        results_upper = find_query("GOOD", SAMPLE_INDEX)
        self.assertEqual(results_lower, results_upper)

    def test_empty_index_returns_empty(self):
        results = find_query("good", {})
        self.assertEqual(results, [])
 
    def test_returns_score_with_url(self):
        results = find_query("good", SAMPLE_INDEX)
        self.assertIsInstance(results[0], tuple)
        self.assertEqual(len(results[0]), 2)

class TestPrintWords(unittest.TestCase):

    def _capture_output(self, word, index):
        """Helper function to run print_word and capture what it prints"""
        captured = StringIO()
        sys.stdout = captured
        print_word(word, index)
        sys.stdout = sys.__stdout__
        return captured.getvalue()
    
    