from kafka3 import KafkaProducer

from app.core.config import kafka_settings


class KafkaProducerService:
    """A class for interacting with Apache Kafka for producing messages."""

    def __init__(self, bootstrap_servers=kafka_settings.bootstrap_servers.split(",")):
        """Initializes an instance with specified library version."""
        self._producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers, api_version=(2, 0, 2)
        )

    def produce_message(self, topic: str, message: str, key: str | None = None) -> None:
        """Produces a message to the specified Kafka topic."""
        self._producer.send(
            topic=topic,
            value=message.encode("utf-8"),
            key=key.encode("utf-8") if key else None,
        )
        self._producer.flush()  # TODO: delete this
