import unittest
from unittest.mock import MagicMock, patch
from bs4 import BeautifulSoup
 
from crawler import extract_links, extract_text, get_page, crawl

#helper function, returns a beautiful soup oject
def make_soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


class TestGetNewLinks(unittest.TestCase):

# class TestExtractText(unittest.TestCase):

# class TestGetPage(unittest.TestCase):

# class TestCrawl(unittest.TestCase):
