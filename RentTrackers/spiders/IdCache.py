import json
import os


class IdCache:
    """
    Cache for storing post ids that have been encountered during scraping.
    The cache maps an id to a numeric value representing the number of runs since that id was seen.
    Ids are dropped from the cache after they are not seen a threshold number of times.
    The cache is stored on disk as a json file in between runs.
        {
            "6934821057": 0,
            "6934808992": 3,
            "6934998421": 8,
            "6935152441": 2,
            "6935518457": 1
        }
    """

    def __init__(self, path):
        self.path = path
        self.cache = {}
        self.__load_cache__()

    def __load_cache__(self):
        """Load the cache from a file."""
        if os.path.isfile(self.path):
            with open(self.path, "r") as f:
                cache = json.load(f)
                self.cache = {int(k): v for k, v in cache.items()}

    def add(self, e):
        """Add an item to the cache."""
        self.cache[e] = -1

    def contains(self, e):
        """Check if an item is in the cache. If it is, reset its check count."""
        if e in self.cache:
            self.cache[e] = -1
            return True
        else:
            return False

    def write_cache(self):
        """Write the cache out to its file."""
        new_cache = {post_id: n + 1 for post_id, n in self.cache.items() if n < 10}
        with open(self.path, "w") as f:
            json.dump(new_cache, f, indent=0)
