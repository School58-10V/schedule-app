import json
from typing import Optional


class Configuration:
    @classmethod
    def configuration(cls, path: Optional[str] = './config.json'):
        with open(path) as file:
            return json.load(file)
