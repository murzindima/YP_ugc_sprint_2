from functools import wraps

from logger import logger


def coroutine(func):
    """
    A decorator for creating coroutines.

    This decorator is used to initialize coroutines. It 'primes' the coroutine by
    automatically advancing it to its first `yield` statement, making the coroutine
    ready to accept input. This is a common pattern in coroutine initialization.

    Parameters:
    func (callable): The coroutine function to be decorated.

    Returns:
    callable: The primed coroutine ready for use.
    """

    @wraps(func)
    def inner(*args, **kwargs):
        """
        Initializes and primes the coroutine.

        This inner function creates a coroutine instance from the provided function,
        advances it to the first `yield`, and then returns this primed coroutine.

        Parameters and Return:
        Same as the coroutine function `func`.
        """
        fn = func(*args, **kwargs)
        next(fn)
        return fn

    return inner


def backoff_handler(details):
    """
    Logs warnings on retry attempts in the decorated function.

    This function is used as a callback in backoff strategies. It logs a warning
    message each time the decorated function retries after an exception, indicating
    the number of tries and the wait time before the next attempt.

    Parameters:
    details (dict): A dictionary containing context details of the retry operation.
    """
    logger.warning(
        "Backing off {wait:0.1f} seconds after {tries} tries calling {target}".format(
            **details
        )
    )


def success_handler(details):
    """
    Logs a message on successful execution after retries.

    This function logs an informational message when the decorated function succeeds
    after one or more retry attempts. It provides details about the successful attempt.

    Parameters:
    details (dict): A dictionary containing context details about the successful retry.
    """
    logger.info("Function {target} succeeded after {tries} tries".format(**details))


def giveup_handler(details):
    """
    Logs an error when the decorated function gives up after retries.

    This function logs an error message when the retry strategy gives up after
    a specified number of attempts. It provides details about the attempted retries
    and the final failure.

    Parameters:
    details (dict): A dictionary containing context details about the failed retries.
    """
    logger.error("Function {target} gave up after {tries} tries".format(**details))
