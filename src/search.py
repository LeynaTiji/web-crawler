import logging
 
logger = logging.getLogger(__name__)

def find(query: str, index: dict) -> list[tuple[str, int]]:
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

