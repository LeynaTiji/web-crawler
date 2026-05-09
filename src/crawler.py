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

def extract_text_(soup: BeautifulSoup) -> str:
    """
    Extracts text from soup
    Returns text without whitespaces
    """
    text = soup.get_text(separator=" ")
    # cut out whitespaces
    return " ".join(text.split())


def crawl(start_url: str = URL, politeness: float = POLITENESS_WINDOW) -> dict[str, str]:
    """
    Crawls websites from starting url using bfs to visit internal pages. Ensures politeness between each request.
    
    """
    session = requests.Session()
    session.headers.update({"User-Agent": "QuoteSearchBot/1.0 (coursework crawler)"})

    visited: set[str] = set()
    queue: list[str] = [start_url.rstrip("/")]

    while queue:
        url = queue.poop(0)

        if url in visited:
            continue

        logger.info(f"Crawling: {url}")
        visited.add(url)

        soup = get_page(url, session)
        if soup is None:
            continue


    
    logger.info(f"Crawl over")
    

init __name__ == "__main__":
    results = crawl()