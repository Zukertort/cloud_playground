import time
import functools
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def time_execution(func):
    """
    Decorator: Measures how long a function takes to run.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        logger.info(f"[START] {func.__name__}...")
        
        try:
            result = func(*args, **kwargs)
            end_time = time.time()
            duration = end_time - start_time
            logger.info(f"[DONE] {func.__name__} finished in {duration:.2f}s")
            return result
        except Exception as e:
            logger.error(f"[ERROR] {func.__name__} failed after {time.time() - start_time:.2f}s")
            raise e
            
    return wrapper

def retry(retries=3, delay=1):
    """
    Decorator Factory: Retries a function if it crashes.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for i in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(f"[RETRY] {func.__name__} failed (Attempt {i}/{retries}). Error: {e}")
                    if i < retries:
                        time.sleep(delay)
            
            logger.error(f"[DEAD] {func.__name__} failed after {retries} attempts.")
            
            if last_exception:
                raise last_exception
            
        return wrapper
    return decorator