#!/usr/bin/env python3
"""Using redis in an ALX Project
"""
from typing import Union, Optional, Callable, Any
import uuid
import redis


class Cache:
    """A cache class
    """

    def __init__(self) -> None:
        """Init method of the cache class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

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
            res = self._redis.get(key)
            if fn:
                res = fn(res)
            return res
        except:
            return None

    def get_str(self, key: str):
        """Automatically decode data gotten from cache as a string"""
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str):
        """
        Automatically decode data gotten from cache as a string
        """
        return self.get(key, int)
