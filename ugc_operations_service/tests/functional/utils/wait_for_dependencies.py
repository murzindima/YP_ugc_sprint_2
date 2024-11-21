import asyncio
import logging
import time

from src.db.mongo import get_mongo_client


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

    mongo_client = get_mongo_client()
    if not check_connection(mongo_client.server_info(), "MongoDB"):
        logging.error("Failed to establish a connection to MongoDB. Exiting...")
        exit(1)
