import json


class Config:
    def __init__(self):
        self.config = self._load_config()

    def get(self, key):
        return self.config[key]

    def set(self, key, value):
        self.config[key] = value
        self._save_config()

    def _load_config(self):
        with open(".config.json") as f:
            return json.load(f)

    def _save_config(self):
        with open(".config.json", "w") as f:
              json.dump(self.config, f)

