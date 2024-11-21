import logging
import sys

logger = logging.getLogger("etl_application")
logger.setLevel(logging.INFO)

sh = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    "%(asctime)s %(levelname)-8s [%(filename)-16s:%(lineno)-5d] %(message)s",
)
sh.setFormatter(formatter)
logger.addHandler(sh)
