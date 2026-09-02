import functools
import time
from src.logging_setup import get_logger, generate_run_id


def pipeline(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        run_id = generate_run_id()       
        log = get_logger(func.__module__, run_id=run_id)
        log.info(f"START {func.__name__}")  

        start = time.time()
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            log.error(f"FAIL {func.__name__}: {e}")  
            raise                            
        finally:
            elapsed = time.time() - start
            log.info(f"DONE {func.__name__} "
                      f"{elapsed*1000:.1f}ms")  

        return result

    return wrapper