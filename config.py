import json
from typing import Optional


class Configuration:
    def __init__(self, path: Optional[str] = './config.json'):
        with open(path) as file:
            self.__cfg = json.load(file)

    def get_configuration(self):
        return self.__cfg
