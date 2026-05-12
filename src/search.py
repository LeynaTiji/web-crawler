import logging
import math
 
logger = logging.getLogger(__name__)

def find_query(query: str, index: dict) -> list[tuple[str, int]]:
    """
    Find all pages containing every word in the query.

    Returns a list of urls and totals, sorted by highest score first.
    """
    words = query.lower().split()
 
    if not words:
        return []
    
    # get urls in for word in words, else empty
    pages = []
    for word in words:
        if word not in index:
            logger.info(f"'{word}' not found in index")
            return []
        pages.append(set(index[word].keys()))

    # query to find instersection of words
    common_pages = pages[0].intersection(*pages[1:])

    if not common_pages:
        return []
    
    #rank by page with highest frequency of query 
    score = []
    for url in common_pages:
        total_score = sum(index[word][url]["freq"] for word in words)
        score.append((url, total_score))
 
    # Sort highest score first
    score.sort(key=lambda x: x[1], reverse=True)
    return score

def print_word(query: str, index: dict) -> None:
    """
    Print inverted index for a given word, showing page, frequency and position of word.
    """

    query = query.lower().strip()

    if not query:
        print("Please provide a word to look up.")
        return
    
    if query not in index:
        print(f"Word '{query}' not found in index.")
        return
    
    entries = index[query]
    print(f"\nInverted index for '{query}' ({len(entries)} page(s)):\n")

    for url, data in entries.items():
        freq = data["freq"]
        positions = data["positions"]
        print(f"  {url}")
        print(f"    Frequency : {freq}")
        print(f"    Positions : {positions}")
        print()   
        
def compute_TFIDF(word: str, url: str, index: dict, total_pages: int):
    """
    Computes the TF-IDF score for a word in a specific page.
    The implementation of TF-IDF comes from https://www.geeksforgeeks.org/machine-learning/understanding-tf-idf-term-frequency-inverse-document-frequency/

    TF stands for term frequency and measures how often a word appears in a page divided by
    by the total number of terms in a page

    IDF stands for Inverse Document Frequency which is the log of the total pages divided by 
    how many pages contain the word.

    Returns computed TF-IDF score

    """
    frequency = index[word][url]["freq"]
    total_pos = len(index[word][url]["positions"])

    # computes TF 
    tf = frequency / total_pos if total_pos > 0 else 0

    # computes IDF 
    pages_with_word = len(index[word])
    idf = math.log(total_pages / (1 + pages_with_word))

    #higher the value the more 
    return tf * idf

