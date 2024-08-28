#!/usr/bin/env python3
"""Using redis in an ALX Project
"""
from typing import Union, Optional, Callable, Any
import uuid
import redis
from functools import wraps

def count_calls(method: Callable) -> Callable:
    """
    Count the ammount of calls made to a method
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper

def call_history(method: Callable) -> Callable:
    """
    Stores the history of calls for a particular function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.rpush(f"{key}:inputs", str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(f"{key}:outputs", str(output))
        return output
    return wrapper



class Cache:
    """A cache class
    """

    def __init__(self) -> None:
        """Init method of the cache class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores new data into the cache storage
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """Gets a value from the cache and optionally converts it
                to it's original value using the callable argument "fn"
        """
        try:
            data = self._redis.get(key)
        except:
            return None
        if fn:
            data = fn(data)
        return data

    def get_str(self, key: str):
        """Automatically decode data gotten from cache as a string"""
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str):
        """
        Automatically decode data gotten from cache as a string
        """
        return self.get(key, int)
