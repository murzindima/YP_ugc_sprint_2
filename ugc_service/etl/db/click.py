import uuid

import backoff
from clickhouse_driver import connect
from clickhouse_driver.dbapi.errors import OperationalError
from clickhouse_driver.errors import NetworkError
from core.config import ClickSettings
from core.logger import get_logger
from dateutil.parser import parse

from .abc import AbstractDB

settings = ClickSettings()
logger = get_logger()


class ClickDB(AbstractDB):
    def insert(self, table: str, batch: list):
        """Forming an insertion string in the database."""
        query = f"INSERT INTO {settings.DATABASE}.{table} "
        colums_table = list(batch[0].keys())
        values_table = []
        for row in batch:
            unit = []
            for key in colums_table:
                value = row[key]
                if value is None:
                    value = "NULL"
                if key == "created_at":
                    value = parse(value)
                    value = str(value.date()) + " " + str(value.time())
                unit.append(value)
            unit.append(str(uuid.uuid4()))
            values_table.append(f"{tuple(unit)}")
        colums_table.append("uuid")
        query += f"({', '.join(colums_table)}) VALUES {', '.join(values_table)}"
        query = query.replace("""'NULL'""", """NULL""")
        return self.__execute(query)

    def create(self, query):
        """Method for executing raw queries."""
        try:
            self.__execute(query)
            return True
        except Exception as e:
            logger.error(f"Error while creating table: {e}")
            return False

    @backoff.on_exception(
        backoff.expo,
        (ConnectionError, NetworkError, OperationalError),
        raise_on_giveup=False,
        logger=logger,
    )
    def __execute(self, query: str):
        with connect(f"clickhouse://{settings.CONNECT}:{settings.PORT}") as conn:
            cursor = conn.cursor()
            cursor.execute(query)
