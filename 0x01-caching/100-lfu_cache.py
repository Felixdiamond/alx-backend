#!/usr/bin/env python3
""" LFUCache module
"""

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """LFUCache class that inherits from BaseCaching and is a caching system

    This caching system uses a least-frequently-used algorithm
    """
    def __init__(self):
        """Initialize
        """
        super().__init__()
        self.queue = []
        self.frequency = {}

    def put(self, key, item):
        """Assign to the dictionary self.cache_data the item value for the key

        If key or item is None, this method should not do anything

        If the number of items in self.cache_data is higher that
        BaseCaching.MAX_ITEMS:
            - you must discard the least frequency used item (LFU algorithm)
            - if you find more than 1 item to discard, you must use the LRU
              algorithm to discard only the least recently used
            - you must print DISCARD: with the key discarded and following by
              a new line

        Args:
            key: key for the cache_data dictionary
            item: value for the cache_data dictionary
        """
        if key is not None and item is not None:
            if len(self.cache_data) == BaseCaching.MAX_ITEMS:
                if key not in self.cache_data:
                    min_freq = min(self.frequency.values())
                    lfu_items = [k for k, v in self.frequency.items()
                                 if v == min_freq]
                    if len(lfu_items) == 1:
                        discard = lfu_items[0]
                    else:
                        for k in self.queue:
                            if k in lfu_items:
                                discard = k
                                break
                    del self.cache_data[discard]
                    del self.frequency[discard]
                    self.queue.remove(discard)
                    print(f"DISCARD: {discard}")
            if key in self.cache_data:
                self.queue.remove(key)
            else:
                self.frequency[key] = 0
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
            value = self.cache_data.get(key)
            if value is not None:
                self.queue.remove(key)
                self.queue.append(key)
                self.frequency[key] += 1
            return value
        return None

