import time
import logging

from elasticsearch import Elasticsearch
from redis import Redis

from ..settings import test_settings


def check_connection(
    ping_function, service_name, max_retries=10, initial_sleep_interval=3
):
    sleep_interval = initial_sleep_interval
    for attempt in range(max_retries):
        try:
            if ping_function():
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

    es_client = Elasticsearch(hosts=test_settings.es_url, verify_certs=False)
    if not check_connection(es_client.ping, "Elasticsearch"):
        logging.error("Failed to establish a connection to Elasticsearch. Exiting...")
        exit(1)

    redis_client = Redis(host=test_settings.redis_host, port=test_settings.redis_port)
    if not check_connection(redis_client.ping, "Redis"):
        logging.error("Failed to establish a connection to Redis. Exiting...")
        exit(1)
