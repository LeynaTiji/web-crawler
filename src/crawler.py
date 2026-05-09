import requests
from bs4 import BeautifulSoup

import logging
from urllib.parse import urljoin, urlparse

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

URL = "https://quotes.toscrape.com"
# 6 seconds between requests
POLITENESS_WINDOW = 6 

def get_page(url: str, session: requests.session) -> BeautifulSoup | None :
    """
    Fetches a single page of url.
    Returns BeautifulSoup object or none if request fails.
    """
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        logger.warning(f"Failed to fetch {url}: {e}")
        return None

def crawl(start_url: str = URL, politeness: float = POLITENESS_WINDOW) -> dict[str, str]:
    session = requests.Session()
    session.headers.update({"User-Agent": "QuoteSearchBot/1.0 (coursework crawler)"})

    

init __name__ == "__main__":
    results = crawl()