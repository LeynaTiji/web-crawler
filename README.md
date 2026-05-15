# Quote Web Crawler

This command line search tool crawls https://quotes.toscrape.com/, building an inverted index of all word occurrences and allows users to search for pages that contain specific phrases or words.

## Project Overview
1. Crawl & Index — the build command crawls every page of the target website, extracts visible text, and constructs an inverted index mapping each word to the pages it appears on. The index stores the frequency and position of every word occurrence, and is saved to JSON file.
2. Search — the load, find, and print commands let users query the saved index. Search results are ranked using TF-IDF (Term Frequency–Inverse Document Frequency).

### Inverted Index Structure 
Each word maps to the pages it appears on, storing frequency and token positions

```json
"honesty": {
    "https://quotes.toscrape.com/author/Andre-Gide": {
      "freq": 1,
      "positions": [125]
    }
  },
```

### TF-IDF Ranking
Results are ranked by TF-IDF score rather than raw frequency:

- **TF (Term Frequency)** = **word frequency / document length** — how often the word appears on a specific page.
- **IDF (Inverse Document Frequency)** = **log(total pages / (1 + pages containing word))** — how rare the word is across the whole site. Common words like "the" score near zero, whilst rarer words produce higher scores.
- **TF-IDF** = **TF × IDF** — pages where the search term is both frequent and rare across the site rank highest.

### Complexity Analysis

Command  | Complexity |  |
-------- | ---------- | ----------- |
Build  | O(N × M) | N = pages, M = average tokens per page|
find  | O(N) | N = number of query terms, dictionary lookup is O(1) |
print | O(N log N + T) | N = pages containing query word, T = total number of pages|

## Running the Web Crawler

1. After cloning repository, create and activate a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

2. Install all dependecies whilst in venv
```bash
pip install -r requirements.txt
```

3. Run the search tool from the project root
```bash
python src/main.py
```

### Commands 

**build**
Crawls website, observing a 6 second politeness window inbetween requests, and saves index to data/index.json
```bash
> build
```

**load**
Loads a previously built index from file. Must run build at least once first.
```bash
> load
```

**find <query>**
Returns all pages containing every word in the query, ranked by TF-IDF relevance.
```bash
> find nonsense
> find good friends
```
Example output:
```bash
> find nonsense 

Pages containing nonsense (ranked by relevance):

  1. https://quotes.toscrape.com/tag/regrets/page/1  (score: 0.044061816334932)
  2. https://quotes.toscrape.com/tag/life  (score: 0.007128909855359368)
  3. https://quotes.toscrape.com/tag/life/page/1  (score: 0.007128909855359368)
```

**print <word>**
```bash
> print love
> print happiness
```
Example output:
```bash
> print love

Inverted index for 'love' (115 page(s)):

  https://quotes.toscrape.com/tag/lack-of-love/page/1
    Frequency : 5
    Positions : [11, 18, 39, 40, 47]

  https://quotes.toscrape.com/tag/marriage/page/1
    Frequency : 4
    Positions : [16, 37, 38, 45]

  https://quotes.toscrape.com/tag/unhappy-marriage/page/1
    Frequency : 4
    Positions : [17, 38, 39, 46]
```
**help**
Lists all available commands.

**quit**/**exit**
Exits the program.

## Testing
Run the full test suite from the project root:
```bash
pytest tests/ -v
```
Run with coverage report:
```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```
Run a specific test file:
```bash
pytest tests/<test_file_name>.py -v
```

### Test Structure

| File | Coverage | 
-------- | ---------- |
test_crawler.py | Unit tests for page fetching, link and text extraction|
test_indexer.py| Unit tests for tokenisation, build index, save and load | 
test_search.py| Unit tests for TF-IDF, find, and print|

Tests use unittest.mock to avoid real HTTP requests