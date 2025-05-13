import time
from contextlib import contextmanager
from functools import wraps
from loguru import logger


@contextmanager
def measure_time(task_name=""):
    """
    A context manager to measure the execution time of a code block.

    :param task_name: A descriptive name for the task being measured.
    :type task_name: str
    :yield: Executes the block of code wrapped by the context manager.
    :example:

        with measure_time("Training model"):
            model.fit(X, y)
    """
    start_time = time.time()
    try:
        yield
    finally:
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"{task_name} took {execution_time:.2f} seconds to execute.")


def timeit(func):
    """
    A decorator to measure and log the execution time of a function.

    :param func: The function whose execution time is to be measured.
    :type func: callable
    :return: A wrapped function that logs its execution duration via loguru.
    :rtype: callable
    :example:

        @timeit
        def process_data():
            ...

    The log output will be of the format:
        "Function process_data Took 0.1234 seconds"
    """
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        logger.info(f'Function {func.__name__} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper
