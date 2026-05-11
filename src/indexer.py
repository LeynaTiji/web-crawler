import json
import re
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

INDEX_PATH = Path("data/index.json")

def tokenise(text: str) -> list[str]:
    """
    Split text into a list of tokens. Make the text lowercase and remove punctuation or whitespace.
    Return tokens
    """
    # line taken from https://algodaily.com/lessons/introducing-search-engine-833b9a7b
    # finds sequence of letters and digits only
    raw_tokens = re.findall(r"[a-z0-9]+", text.lower())
    return raw_tokens


def build_index(pages: dict[str, str]) -> dict:
    """
    Builds an inverted index of urls to page text
    
    Returns the completed index dict.
    """

    index = {}

    for url, text in pages.items():
        token = tokenise(text)