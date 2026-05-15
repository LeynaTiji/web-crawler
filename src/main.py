import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

from crawler import crawl, URL
from indexer import build_index, save_index, load_index
from search import find_query, print_word

BANNER = """
╔══════════════════════════════════════╗
║        Quote Search Tool             ║
║  Type 'help' to see all commands     ║
╚══════════════════════════════════════╝
"""
 
HELP_TEXT = """
Available commands:
  build              Crawl the website and build the index
  load               Load the index from file, only works if build has been run previously
  print <word>       Print index entry for a word  (e.g. print nonsense)
  find <query>       Find pages matching query      (e.g. find good friends)
  help               Show this help message
  quit / exit        Exit the program
"""

def cmd_build(index_state: dict) -> dict:
    pages = crawl(URL)
    if not pages:
        print("Crawl returned no pages.")
        return index_state
    index = build_index(pages)
    save_index(index)

    print(f"\nCrawling done. Indexed {len(pages)} pages and {len(index)} unique words.")
    return index

def cmd_find(args: str, index: dict):
    """
    Find pages containing all words in query
    """
    if not index:
        print("No index loaded. Run 'build' or 'load' first.")
        return
    
    query = args.strip()
    if not query:
        print("Usage: find <query>  (e.g. find love, find happy friends)")
        return
    
    results = find_query(query, index)
    if not results:
        print(f"No pages found containing all words in '{query}'.")
        return
    
    print(f"\nPages containing {query} "
          f"(ranked by relevance):\n")
    for rank, (url, score) in enumerate(results, start=1):
        print(f"  {rank}. {url}  (score: {score})")
    print()
    
def cmd_print(args: str, index: dict):
    """
    Print index entry for inputted word
    """
    if not index:
        print("No index loaded. Run 'build' or 'load' first.")
        return
    if not args.strip():
        print("Usage: print <word>  (e.g. print indifference)")
        return
    # print takes a single word
    words = args.strip().split()
    if len(words) > 1:
        print(f"Note: 'print' only looks up one word. Showing results for '{words[0]}' instead.")
    print_word(words[0], index)

def cmd_load(index_state: dict) -> dict:
    """
    Load index from file and returns it
    """
    try:
        index = load_index()
        print(f"Index loaded.")
        return index
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return index_state

def run_shell():
    """
    Reads command line arguements. 
    """

    print(BANNER)

    index = {}

    while True:
        raw = input("> ").strip()
        if not raw:
            continue

        # split into command and the rest of the line
        parts = raw.split(maxsplit=1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        if command == "build":
            index = cmd_build(index)
        elif command == "load":
            index = cmd_load(index)
        elif command == "print":
            cmd_print(args, index)
        elif command == "find":
            cmd_find(args, index)
        elif command == "help":
            print(HELP_TEXT) 
        elif command in ("quit", "exit"):
            print("Goodbye.")
            sys.exit(0)
 
        else:
            print(f"Unknown command '{command}'. Type 'help' to see available commands.")
 
if __name__ == "__main__":
    run_shell()