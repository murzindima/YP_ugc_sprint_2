import asyncio
import time
import logging

from redis import Redis
from sqlalchemy import text

from tests.functional.settings import test_settings
from src.db.postgres import engine
from src.core.config import redis_settings


async def check_postgres_connection():
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    await engine.dispose()
    return True


def check_connection(
    ping_function,
    service_name,
    max_retries=10,
    initial_sleep_interval=3,
    is_async=False,
):
    sleep_interval = initial_sleep_interval
    for attempt in range(max_retries):
        try:
            if is_async:
                success = asyncio.run(ping_function())
            else:
                success = ping_function()

            if success:
                logging.info(f"Successfully connected to {service_name}.")
                return True
        except Exception as e:
            logging.warning(
                f"Attempt {attempt + 1} to connect to {service_name} failed: {e}"
            )
        time.sleep(sleep_interval)
        sleep_interval *= 2

    logging.error(
        f"Maximum retry attempts reached. Could not connect to {service_name}."
    )
    return False


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    redis_client = Redis(host=redis_settings.host, port=redis_settings.port)
    if not check_connection(redis_client.ping, "Redis"):
        logging.error("Failed to establish a connection to Redis. Exiting...")
        exit(1)

    if not check_connection(check_postgres_connection, "PostgreSQL", is_async=True):
        logging.error("Failed to establish a connection to PostgreSQL. Exiting...")
        exit(1)
