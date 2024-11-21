import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from redis.asyncio import Redis

from functional.settings import test_settings


@pytest_asyncio.fixture
async def es_client():
    client = AsyncElasticsearch(hosts=test_settings.es_url, verify_certs=False)
    try:
        yield client
    finally:
        await client.close()


@pytest_asyncio.fixture
async def redis_client():
    client = Redis(host=test_settings.redis_host, port=test_settings.redis_port)
    try:
        yield client
    finally:
        await client.aclose()
