#!/usr/bin/env python3
"""Using redis in an ALX Project
"""
from typing import Union
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
