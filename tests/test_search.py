import unittest

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