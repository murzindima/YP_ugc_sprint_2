from elasticsearch import AsyncElasticsearch

es: AsyncElasticsearch | None = None


async def get_elastic() -> AsyncElasticsearch:
    """
    Get the AsyncElasticsearch instance.

    Returns:
        AsyncElasticsearch: The instance of AsyncElasticsearch.
    """
    return es
