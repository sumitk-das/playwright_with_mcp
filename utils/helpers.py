import os
import time


def get_env(key: str, default: str = "") -> str:
    return os.getenv(key, default)


def timestamp() -> str:
    return time.strftime("%Y%m%d_%H%M%S")
