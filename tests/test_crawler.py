import unittest
from unittest.mock import MagicMock, patch
from bs4 import BeautifulSoup
 
from crawler import get_new_link, extract_text, get_page, crawl

#helper function, returns a beautiful soup oject
def make_soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")

class TestGetNewLinks(unittest.TestCase):

    def test_returns_internal_links(self):
        soup = make_soup('<a href="/page/2/">next</a>')
        links = get_new_link(soup, "https://quotes.toscrape.com")
        self.assertIn("https://quotes.toscrape.com/page/2", links)


# class TestExtractText(unittest.TestCase):

# class TestGetPage(unittest.TestCase):

# class TestCrawl(unittest.TestCase):
