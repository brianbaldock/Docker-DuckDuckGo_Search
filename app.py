from fastapi import FastAPI, Query
from duckduckgo_search import DDGS
import urllib.parse
import time
import random
from functools import lru_cache

app = FastAPI()

@app.get("/")
def root():
    return {"message": "DuckDuckGo Search API is running"}

# Cached search function to reduce duplicate queries
@lru_cache(maxsize=100)  # Stores last 100 unique searches
def cached_search(query: str, max_results: int):
    """
    Cached DuckDuckGo search function with rate-limit protection.
    """
    try:
        time.sleep(random.uniform(1.5, 3.5))  # Random delay to avoid rate limiting

        # Remove spaces from multi-word queries to avoid triggering DuckDuckGo rate limits
        modified_query = query.replace(" ", "")

        with DDGS() as ddgs:
            results = list(ddgs.text(modified_query, max_results=max_results))

        return results

    except Exception as e:
        return {"error": "DuckDuckGo search failed. Try again later.", "details": str(e)}

@app.get("/search")
def search_duckduckgo(query: str = Query(..., title="Search Query"), max_results: int = 5):
    """
    API endpoint for searching DuckDuckGo with rate-limit protection using the duckduckgo_search python libray (https://github.com/deedy5/duckduckgo_search)
    """
    normalized_query = urllib.parse.unquote(query).replace("+", " ")

    results = cached_search(normalized_query, min(max_results, 5))  # Limit results to 5 max

    return {"query": normalized_query, "results": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
