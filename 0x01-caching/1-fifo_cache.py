#!/usr/bin/env python3
""" FIFOCache module
"""

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """FIFOCache class that inherits from BaseCaching and is a caching system

    This caching system uses a first-in, first-out algorithm
    """
    def __init__(self):
        """Initialize
        """
        super().__init__()
        self.queue = []

    def put(self, key, item):
        """Assign to the dictionary self.cache_data the item value for the key

        If key or item is None, this method should not do anything

        If the number of items in self.cache_data is higher that
        BaseCaching.MAX_ITEMS:
            - you must discard the first item put in cache (FIFO algorithm)
            - you must print DISCARD: with the key discarded and following by
              a new line

        Args:
            key: key for the cache_data dictionary
            item: value for the cache_data dictionary
        """
        if key is not None and item is not None:
            if len(self.cache_data) == BaseCaching.MAX_ITEMS:
                if key not in self.cache_data:
                    discard = self.queue.pop(0)
                    del self.cache_data[discard]
                    print(f"DISCARD: {discard}")
            self.queue.append(key)
            self.cache_data[key] = item

    def get(self, key):
        """Return the value in self.cache_data linked to key

        If key is None or if the key doesn’t exist in self.cache_data,
        return None

        Args:
            key: key for the cache_data dictionary

        Returns:
            Value in self.cache_data linked to key
        """
        if key is not None:
            return self.cache_data.get(key)
        return None

