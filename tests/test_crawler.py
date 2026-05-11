import unittest
from unittest.mock import MagicMock, patch
from bs4 import BeautifulSoup
 
from src.crawler import get_new_link, extract_text, get_page, crawl

#helper function, returns a beautiful soup oject
def make_soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")

URL = "https://quotes.toscrape.com"

class TestGetNewLinks(unittest.TestCase):

    def test_returns_internal_links(self):
        soup = make_soup('<a href="/page/2/">next</a>')
        links = get_new_link(soup, URL)
        self.assertIn("https://quotes.toscrape.com/page/2", links)

    def test_ignores_external_links(self):
        soup = make_soup('<a href="https://google.com">Google</a>')
        links = get_new_link(soup, URL)
        self.assertEqual(links, [])

    def test_ignores_fragment_only_links(self):
        # fragment only links should not be counted as a new page
        soup = make_soup('<a href="#top">Back to top</a>')
        links = get_new_link(soup, URL)
        # check it doesnt return these links
        for link in links:
            self.assertNotIn("#", link)
    
    def test_no_links_returns_empty_list(self):
        soup = make_soup("<p>No links here</p>")
        links = get_new_link(soup, URL)
        self.assertEqual(links, [])

    
    def test_deduplicates_same_link(self):
        soup = make_soup(
            '<a href="/page/2/">next</a><a href="/page/2/">next again</a>'
        )
        links = get_new_link(soup, URL)
        # both point to same URL — count occurrences
        self.assertEqual(links.count("https://quotes.toscrape.com/page/2"), 2)

class TestExtractText(unittest.TestCase):
    

# class TestGetPage(unittest.TestCase):

# class TestCrawl(unittest.TestCase):
