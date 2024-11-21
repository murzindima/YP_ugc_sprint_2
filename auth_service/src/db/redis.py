from redis.asyncio import Redis

redis: Redis | None = None


async def get_redis() -> Redis:
    """Get the Redis instance."""
    return redis
