import logging
import sys

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


BANNER = """
╔══════════════════════════════════════╗
║        Quote Search Tool             ║
║  Type 'help' to see all commands     ║
╚══════════════════════════════════════╝
"""
 
HELP_TEXT = """
Available commands:
  build              Crawl the website and build the index
  load               Load the index from disk
  print <word>       Print index entry for a word  (e.g. print good)
  find <query>       Find pages matching query      (e.g. find good morning)
  help               Show this help message
  quit / exit        Exit the program
"""
 
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
        #     index = build(index)
            print("build")
 
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