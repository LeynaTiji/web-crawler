import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

from crawler import crawl, URL
from indexer import build_index, save_index

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

INDEX_PATH = Path("data/index.json")

def build(index_state: dict) -> dict:
    pages = crawl(URL)
    if not pages:
        print("Crawl returned no pages.")
        return index_state
    index = build_index(pages)
    save_index(index, INDEX_PATH)

    print(f"\nCrawling done. Indexed {len(pages)} pages and {len(index)} unique words.")
    return index

def run_shell():
    """
    Reads commands 
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
            index = build(index)
        # elif command == "load":
        #     index = load(index)
        # elif command == "print":
        #     print(args, index)
        # elif command == "find":
        #     find(args, index)
        elif command == "help":
            print(HELP_TEXT)
 
        elif command in ("quit", "exit"):
            print("Goodbye.")
            sys.exit(0)
 
        else:
            print(f"Unknown command '{command}'. Type 'help' to see available commands.")
 
if __name__ == "__main__":
    run_shell()