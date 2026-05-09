import requests
from bs4 import BeautifulSoup
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

URL = "https://quotes.toscrape.com"
# 6 seconds between requests
POLITENESS_WINDOW = 6 

def get_page(url: str, session: requests.session):
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        logger.warning(f"Failed to fetch {url}: {e}")
        return None
   