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

def save_index(index: dict, path: Path = INDEX_PATH):
    """
    Stores inex in JSON file. 
    """
    # implemented using https://www.geeksforgeeks.org/python/json-dump-in-python/
    with open(path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)
    logger.info(f"Index saved to {path}")

def load_index(path: Path = INDEX_PATH) -> dict:
    """
    Load the index from json file
    if index doesnt exist, raise error
    """
    if not path.exists():
        raise FileNotFoundError(
            f"No index found at {path}. Run 'build' first."
        )
    
    with open(path, "r", encoding="utf-8") as f:
        index = json.load(f)
    logger.info(f"Index loaded from {path} ({len(index)} words)")
    return index

def build_index(pages: dict[str, str]) -> dict:
    """
    Builds an inverted index of urls to page text, storing statistics about the words.
    
    Returns the completed index dict.
    """

    index = {}
    page_lengths = {}  

    for url, text in pages.items():
        tokens = tokenise(text)
        #store total tokens per page
        page_lengths[url] = len(tokens)

        for position, word in enumerate(tokens):
            if word not in index:
                index[word] = {}

            if url not in index[word]:
                index[word][url] = {"freq": 0, "positions": []}
 
            index[word][url]["freq"] += 1
            index[word][url]["positions"].append(position)      
    
    index["page_lengths"] = page_lengths

    logger.info(f"Index built: {len(index)} unique words")
    return index
