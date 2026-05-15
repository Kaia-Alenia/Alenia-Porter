import os
import sys
import functools

def ignite():
    os.environ["ALENIA_ZENITH_ACTIVE"] = "true"
    sys.modules["zenith"] = sys.modules[__name__]
    return True

def zenith_cache(func):
    @functools.lru_cache(maxsize=128)
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

def safe_execution(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            from porter_logic import log_error_to_file
            log_error_to_file(f"Zenith Shield caught: {str(e)}")
            return None
    return wrapper
