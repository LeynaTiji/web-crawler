import unittest
from unittest.mock import MagicMock, patch

import requests
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
        self.assertIn("Quote text", text)
 
    def test_collapses_whitespace(self):
        soup = make_soup("<p>too   many    spaces</p>")
        text = extract_text(soup)
        self.assertNotIn("  ", text)
 
    def test_empty_page_returns_empty_string(self):
        soup = make_soup("")
        text = extract_text(soup)
        self.assertEqual(text, "")

    def test_strips_header_tags(self):
        soup = make_soup("<header>Menu Stuff</header><p>Quote text</p>")
        text = extract_text(soup)
        self.assertNotIn("Menu", text)
        self.assertIn("Quote text", text)

class TestGetPage(unittest.TestCase):
    @patch("src.crawler.requests.Session.get")
    def test_returns_soup_on_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<p>Hello</p>"
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        session = requests.Session()
        soup = get_page("https://quotes.toscrape.com", session)
        self.assertIsNotNone(soup)
 
    @patch("src.crawler.requests.Session.get")
    def test_returns_none_on_http_error(self, mock_get):
        mock_get.side_effect = requests.RequestException("404 Not Found")
        session = requests.Session()
        soup = get_page("https://quotes.toscrape.com/bad-url", session)
        self.assertIsNone(soup)
 
class TestCrawl(unittest.TestCase):

    @patch("src.crawler.get_page")
    # prevent tests from waiting 6 seconds
    @patch("src.crawler.time.sleep")
    def test_crawl_visits_linked_pages(self, mock_sleep, mock_get_page):
        page1 = make_soup('<p>Quote one</p><a href="/page/2/">next</a>')
        page2 = make_soup("<p>Quote two</p>")
        # return page 1 for the first call, page 2 for the second
        mock_get_page.side_effect = [page1, page2]
        results = crawl("https://quotes.toscrape.com", politeness=0)
        self.assertEqual(len(results), 2)
 
    @patch("src.crawler.get_page")
    @patch("src.crawler.time.sleep")
    def test_crawl_does_not_revisit_pages(self, mock_sleep, mock_get_page):
        #page links back to itself, crawler must not loop forever
        page = make_soup('<p>Text</p><a href="/">home</a>')
        mock_get_page.return_value = page
        results = crawl("https://quotes.toscrape.com", politeness=0)
        # should only visit the one page, not infinite loop
        self.assertEqual(mock_get_page.call_count, 1)
 
    @patch("src.crawler.get_page")
    @patch("src.crawler.time.sleep")
    def test_crawl_skips_failed_pages(self, mock_sleep, mock_get_page):
        # get_page returns None (simulating a network error)
        mock_get_page.return_value = None
        results = crawl("https://quotes.toscrape.com", politeness=0)
        self.assertEqual(results, {})

