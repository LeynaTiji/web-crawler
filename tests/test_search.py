import unittest
import math
from io import StringIO
import sys

from src.indexer import build_index
from src.search import find_query, print_word, compute_TFIDF

SAMPLE_INDEX = {
    "page_lengths": {
        "https://example.com/page1": 50,
        "https://example.com/page2": 30,
    },
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

    def test_prints_word_info(self):
        output = self._capture_output("good", SAMPLE_INDEX)
        self.assertIn("good", output)
        self.assertIn("https://example.com/page1", output)

    def test_word_not_in_index_prints_message(self):
        output = self._capture_output("nonsense", SAMPLE_INDEX)
        self.assertIn("not found ", output)

    def test_empty_word_prints_usage_message(self):
        output = self._capture_output("", SAMPLE_INDEX)
        self.assertIn("Please provide", output)
 
    def test_case_insensitive(self):
        output_lower = self._capture_output("good", SAMPLE_INDEX)
        output_upper = self._capture_output("GOOD", SAMPLE_INDEX)
        self.assertEqual(output_lower, output_upper)

class TestTFIDF(unittest.TestCase):

    def test_returns_float(self):
        score = compute_TFIDF("good", "https://example.com/page1", SAMPLE_INDEX, 2)
        self.assertIsInstance(score, float)
 
    def test_higher_frequency_gives_higher_score(self):
        score1 = compute_TFIDF("good", "https://example.com/page1", SAMPLE_INDEX, 10)
        score2 = compute_TFIDF("good", "https://example.com/page2", SAMPLE_INDEX, 10)
        self.assertGreater(score1, score2)
 
    def test_rare_word_scores_higher_idf(self):
        # friends appears in 1 page, good appears in 2 pages
        idf_friends = math.log(2 / (1 + 1))
        idf_good = math.log(2 / (1 + 2))
        self.assertGreater(idf_friends, idf_good)
 
    def test_score_is_zero(self):
        # positions list is empty
        edge_index = {
            "word": {"https://example.com": {"freq": 1, "positions": []}}
        }
        score = compute_TFIDF("word", "https://example.com", edge_index, 1)
        self.assertEqual(score, 0.0)


class TestIntegration(unittest.TestCase):

    def test_build_and_search_pipeline(self):
        """Test full pipeline: index some pages, then search them."""
        pages = {
            "https://example.com/page1": "good friends are hard to find",
            "https://example.com/page2": "good morning is a good greeting",
        }
        index = build_index(pages)
        results = find_query("good", index)
        #both pages should appear in results
        urls = [url for url, _ in results]
        self.assertIn("https://example.com/page1", urls)
        self.assertIn("https://example.com/page2", urls)
        self.assertEqual(len(results), 2)

