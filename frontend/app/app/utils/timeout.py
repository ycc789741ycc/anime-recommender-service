import multiprocessing.pool
import functools
# import signal
# from contextlib import contextmanager


# class TimeoutException(Exception):
#     pass


# @contextmanager
# def time_limit(seconds):
#     def signal_handler(signum, frame):
#         raise TimeoutException("Timed out!")
#     signal.signal(signal.SIGALRM, signal_handler)
#     signal.alarm(seconds)
#     try:
#         yield
#     finally:
#         signal.alarm(0)


def time_limit(max_time_limit):
    """Timeout decorator, parameter in seconds."""
    def time_limit_decorator(item):
        """Wrap the original function."""
        @functools.wraps(item)
        def func_wrapper(*args, **kwargs):
            """Closure for function."""
            pool = multiprocessing.pool.ThreadPool(processes=1)
            async_result = pool.apply_async(item, args, kwargs)
            # raises a TimeoutError if execution exceeds max_time_limit
            return async_result.get(max_time_limit)
        return func_wrapper
    return time_limit_decorator
