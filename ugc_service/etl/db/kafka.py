import json

import backoff
from core.config import KafkaSettings
from core.logger import get_logger
from kafka3 import KafkaConsumer

from .abc import AbstractQueue

kafka_settings = KafkaSettings()
logger = get_logger()


class KafkaQuery(AbstractQueue):
    def __init__(self, topic):
        self.topic = topic

    @backoff.on_exception(backoff.expo, Exception, raise_on_giveup=False, logger=logger)
    def get_consumer(self):
        """Creating a consumer for a specific topic."""
        consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=kafka_settings.SERVERS,
            group_id=self.topic,
            reconnect_backoff_ms=1000,
            reconnect_backoff_max_ms=600000,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            enable_auto_commit=False,
        )
        return consumer
