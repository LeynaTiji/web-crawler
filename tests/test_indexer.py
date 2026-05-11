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

