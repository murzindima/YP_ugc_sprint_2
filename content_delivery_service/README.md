# Async API Sprint 2: Testing and SOLID Principles

## How to run tests:

### Locally:

Please make sure that API, Elasticsearch and Redis are running and available.

Set environment variables if needed.

```shell
# Run poetry shell
$ poetry shell
# Install dependencies
$ poetry install
# Run tests with pytest 
$ pytest tests
```

### In Docker:

```shell
docker-compose up --build --exit-code-from tests
```
Already preconfigured docker-compose.yml file for running tests in Docker.

Environment variables are already set in docker-compose.yml file.

1. RUN_CMD=tests
2. ES_URL=http://elasticsearch:9200
3. REDIS_HOST=redis
4. API_URL=http://api:8000

##  What is under the hood:

1. Tests are written using pytest and pytest-asyncio
2. Tests are located in the tests folder
3. There are three tests files:
    1. test_films.py
    2. test_genres.py
    3. test_persons.py
4. Dependencies
   1. elasticsearch
   2. redis
   3. fastapi
5. Docker-compose file for running tests in Docker
6. Tests using the same Docker image as API
7. What is going on if you run tests in Docker:
    1. API image is built 
    2. Docker-compose file starts three containers:
        1. Redis
        2. Elasticsearch
        3. API
    3. Elasticsearch and Redis containers are started without preconfiguring
    4. Docker-compose file starts tests container
       1. Tests container waits for Elasticsearch and Redis services are up
       2. Tests container configure and fill Elasticsearch with test data
       3. Tests container runs tests
       4. Docker-compose waits for tests container to exit
       5. Docker-compose stops all containers

## Environment variables:

| Value         | Type    | Default               | Description                         |
|:--------------|---------|-----------------------|:------------------------------------|
| RUN_CMD       | string  |                       | Only for run in Docker. Use "tests" |
| ES_URL        | string  | http://localhost:9200 | Elastic Search URL                  |
| REDIS_HOST    | string  | localhost             | Redis hostname                      |
| REDIS_PORT    | int     | 6379                  | Redis port                          |
| API_URL       | string  | http://localhost:8000 | FastAPI URL                         |
| API_BASE_PATH | string  | /api/v1               | API base path with version          |

## Repository Link:
https://github.com/IlyasDevelopment/Async_API_sprint_2
