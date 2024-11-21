import logging
import timeit

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

file_handler = logging.FileHandler("operations.log", mode="w")
file_handler.setFormatter(logging.Formatter("%(message)s"))
logger.addHandler(file_handler)


def set_timer(n=1):
    def decorator(func):
        async def wrapper(self, *args, **kwargs):
            start_time = timeit.default_timer()
            result = await func(self, *args, **kwargs)
            func_time = timeit.default_timer() - start_time
            if n == 1:
                logger.info(
                    f"{self.__class__.__name__}.{func.__name__} execution time: {round(func_time, 5)} seconds"
                )
            else:
                logger.info(
                    f"{self.__class__.__name__}.{func.__name__} avg execution time: {round(func_time/n, 5)} seconds"
                )
            return result

        return wrapper

    return decorator
