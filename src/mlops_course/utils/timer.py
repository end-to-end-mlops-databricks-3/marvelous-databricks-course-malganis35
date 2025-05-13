import time
from contextlib import contextmanager
from functools import wraps
from loguru import logger

@contextmanager
def measure_time(task_name=""):
    """
    A context manager to measure the execution time of a code block.

    Parameters:
    - task_name (str): A name for the task being timed.
    """
    start_time = time.time()
    try:
        yield
    finally:
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"{task_name} took {execution_time:.2f} seconds to execute.")

def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        logger.info(f'Function {func.__name__} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper