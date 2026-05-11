import json
import unittest
from pathlib import Path
import tempfile
 
from src.indexer import tokenise, build_index, save_index

class TestTokenise(unittest.TestCase):
 
    def test_lowercases_words(self):
        self.assertEqual(tokenise("Hello World"), ["hello", "world"])
 
    def test_strips_punctuation(self):
        self.assertEqual(tokenise("Can't you see, silly."), ["can", "t", "you", "see", "silly"])
 
    def test_empty_string_returns_empty_list(self):
        self.assertEqual(tokenise(""), [])
 
    def test_numbers_are_kept(self):
        self.assertIn("42", tokenise("page 42"))
 
    def test_spaces_handled(self):
        result = tokenise("too   many   spaces")
        self.assertEqual(result, ["too", "many", "spaces"])

class TestBuildIndex(unittest.TestCase):

    def setUp(self):
        self.pages = {
            "https://example.com/page1": "good im doing good too",
            "https://example.com/page2": "good morning everyone",
        }
        self.index = build_index(self.pages)

    def test_word_appears_in_correct_pages(self):
        self.assertIn("https://example.com/page1", self.index["good"])
        self.assertIn("https://example.com/page2", self.index["good"])
 
    def test_word_only_in_one_page(self):
        self.assertIn("https://example.com/page1", self.index["doing"])
        self.assertNotIn("https://example.com/page2", self.index.get("doing", {}))
 
    def test_frequency_is_correct(self):
        # good appears twice in page 1
        self.assertEqual(self.index["good"]["https://example.com/page1"]["freq"], 2)
 
    def test_positions_are_recorded(self):
        positions = self.index["good"]["https://example.com/page1"]["positions"]
        # [0,3] position of good
        self.assertEqual(positions, [0, 3])
 
    def test_empty_pages_returns_empty_index(self):
        self.assertEqual(build_index({}), {})
 
    def test_case_insensitive(self):
        index = build_index({"https://example.com": "Good good GOOD"})
        self.assertEqual(index["good"]["https://example.com"]["freq"], 3)

class TestSaveIndex(unittest.TestCase):

    def test_save(self):
        index = {"hello": {"https://example.com": {"freq": 1, "positions": [0]}}}
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "index.json"
            save_index(index, path)

    