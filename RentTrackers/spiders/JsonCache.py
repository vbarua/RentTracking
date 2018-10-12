import json
import os


class JsonCache:

    def __init__(self, path):
        self.path = path
        self.cache = {}
        self.__load_cache__()

    def add(self, e):
        self.cache[e] = 1

    def contains(self, e):
        if e in self.cache:
            self.cache[e] = 1
            return True
        else:
            return False

    def __load_cache__(self):
        if os.path.isfile(self.path):
            with open(self.path, "r") as f:
                post_ids = json.load(f)
                self.cache = {int(pid) : 0 for pid in post_ids}

    def write_cache(self):
        filtered_dict = [pid for pid, v in self.cache.items() if v == 1]
        with open(self.path, "w") as f:
            json.dump(filtered_dict, f, indent=0)
