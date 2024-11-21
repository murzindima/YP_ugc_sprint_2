from abc import ABC, abstractmethod


class AbstractDB(ABC):
    @abstractmethod
    def insert(self, **kwargs):
        pass


class AbstractQueue(ABC):
    @abstractmethod
    def get_consumer(self):
        pass
