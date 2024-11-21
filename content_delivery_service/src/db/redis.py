from redis.asyncio import Redis

redis: Redis | None = None


async def get_redis() -> Redis:
    """
    Get the Redis instance.

    Returns:
        Redis: The instance of the Redis client.
    """
    return redis
