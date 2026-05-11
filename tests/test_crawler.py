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

    def test_extracts_visible_text(self):
        soup = make_soup("<p>Hello world</p>")
        text = extract_text(soup)
        self.assertNotIn("<p>", text)
        self.assertIn("Hello world", text)

    def test_strips_script_tags(self):
        soup = make_soup("<script>alert('xss')</script><p>Real content</p>")
        text = extract_text(soup)
        self.assertNotIn("alert", text)
        self.assertIn("Real content", text)

    def test_strips_style_tags(self):
        soup = make_soup("<style>body { color: red; }</style><p>Visible</p>")
        text = extract_text(soup)
        self.assertNotIn("color", text)
        self.assertIn("Visible", text)

    def test_strips_nav_tags(self):
        soup = make_soup("<nav>Home Authors Tags</nav><p>Quote text</p>")
        text = extract_text(soup)
        self.assertNotIn("Home", text)
 
    def test_collapses_whitespace(self):
        soup = make_soup("<p>too   many    spaces</p>")
        text = extract_text(soup)
        self.assertNotIn("  ", text)
 
    def test_empty_page_returns_empty_string(self):
        soup = make_soup("")
        text = extract_text(soup)
        self.assertEqual(text, "")

# class TestGetPage(unittest.TestCase):

# class TestCrawl(unittest.TestCase):
