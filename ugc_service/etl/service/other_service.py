import uuid

import backoff
import requests
from core.logger import get_logger

logger = get_logger()


@backoff.on_exception(backoff.expo, Exception, raise_on_giveup=False, logger=logger)
def get_data_other_service(url: str, id: uuid.UUID):
    return requests.get(f"{url}{id}").json()
