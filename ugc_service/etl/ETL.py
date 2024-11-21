import os
import sys

sys.path.append(os.getcwd())

from db.click import ClickDB
from db.kafka import KafkaQuery
from core.config import ETLSettings
from service.other_service import get_data_other_service

settings = ETLSettings()

topic = sys.argv[1]


def kafka_parser(values):
    """adding data from other services"""
    movie = {}
    user = {}
    if "movie_id" in values.keys():
        movie = get_data_other_service(settings.CONTENT_API, values["movie_id"])
    if "user_id" in values.keys():
        user = get_data_other_service(settings.USER_API, values["user_id"])
    return values | movie | user


if __name__ == "__main__":
    click = ClickDB()
    kafka = KafkaQuery(topic)

    consumer = kafka.get_consumer()
    count = 0
    batch = []
    for messages in consumer:
        data = kafka_parser(messages.value)
        batch.append(data)
        count += 1
        if count == settings.BATCH_COUNT:
            click.insert(topic, batch)
            consumer.commit()
            count = 0
            batch = []
