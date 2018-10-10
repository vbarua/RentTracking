import json
import os


class JsonCache:

    def __init__(self, path):
        self.path = path
        self.cache = set()
        self.__load_cache__()

    def add(self, e):
        self.cache.add(e)

    def does_not_contain(self, e):
        return e not in self.cache

    def __load_cache__(self):
        if os.path.isfile(self.path):
            with open(self.path, "r") as f:
                self.cache = set(json.load(f))

    def write_cache(self):
        with open(self.path, "w") as f:
            json.dump(list(self.cache), f)
