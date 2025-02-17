# DuckDuckGo Search API Service

A lightweight FastAPI service that uses the [duckduckgo_search](https://github.com/deedy5/duckduckgo_search) Python library to perform DuckDuckGo searches. This repository includes everything needed to build and run the service in a Docker container.

---

## Features

- **DuckDuckGo Search**  
  Performs text searches via DuckDuckGo’s search engine using the `duckduckgo_search` library.

- **FastAPI**  
  A simple RESTful API interface, built with [FastAPI](https://fastapi.tiangolo.com/).

- **Caching & Rate Limit Considerations**  
  Uses `functools.lru_cache` to cache results and a random delay to reduce the chance of rate limiting.

- **Docker-Ready**  
  Includes a Dockerfile and docker-compose.yml for easy containerization and deployment.

---

## Files Overview

- **app.py**  
  Defines two API endpoints:
  - `GET /` – Returns a basic status message.
  - `GET /search` – Accepts `query` and `max_results` (capped at 5) for DuckDuckGo searches.

- **requirements.txt**  
  Lists Python dependencies (FastAPI, Uvicorn, duckduckgo_search).

- **Dockerfile**  
  Builds the Docker image with Python 3.11-slim and installs dependencies.

- **docker-compose.yml**  
  Simplifies running the container with predefined configurations.

---

## Usage

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/duckduckgo-search-api.git
cd duckduckgo-search-api
```

### 2. Build and Run with Docker Compose

```bash
docker-compose up --build
```

This will:
- Build the `ddgs-service:latest` image.
- Start the container.
- Expose the service on [http://localhost:8082](http://localhost:8082).

### 3. Alternatively: Build and Run with Docker CLI

#### Build the image
```bash
docker build -t ddgs-service:latest .
```

#### Run the container
```bash
docker run -d -p 8082:8000 --name ddgs ddgs-service:latest
```

The service will be running on [http://localhost:8082](http://localhost:8082).

---

## API Endpoints

### `GET /`
Returns a simple JSON status message:
```json
{
  "message": "DuckDuckGo Search API is running"
}
```

### `GET /search`
Runs a DuckDuckGo search for the provided `query`.

#### Query Parameters:
- **`query`** (required): A URL-encoded string of the search term.
- **`max_results`** (optional, defaults to 5, capped at 5).

#### Example:
```bash
GET http://localhost:8082/search?query=Microsoft&max_results=3
```

#### Response:
```json
{
  "query": "Microsoft",
  "results": [
    "Result 1",
    "Result 2",
    ...
  ]
}
```

---

## Notes and Limitations

- This service adds a random delay (1.5–3.5 seconds) to help avoid potential rate limiting from DuckDuckGo.
- For repeated searches, an in-memory LRU cache is used (`@lru_cache`) to reduce duplicate requests.
- Only the last 100 unique searches are cached.
- `max_results` is limited to a maximum of **5** to keep responses concise.

---

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit and push your changes.
4. Open a pull request.

Feel free to open an issue if you run into any problems or have questions.
