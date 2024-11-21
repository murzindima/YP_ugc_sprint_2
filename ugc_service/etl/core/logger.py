import logging

from core.config import ETLSettings

setting = ETLSettings()

logging.basicConfig(level=logging.ERROR, filename=setting.LOGGER_PATH)
logger = logging.getLogger("logger")

handler = logging.StreamHandler()
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def get_logger():
    return logger
