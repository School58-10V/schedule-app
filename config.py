import json
from typing import Optional


class Configuration:
    def __init__(self, path: Optional[str] = './config.json'):
        with open(path) as file:
            self.__cfg = json.load(file)

    def get_configuration(self):
        return self.__cfg
    
    def get(self, path: str) -> str:
        points = path.split(".")
        section = self.__cfg.copy()
        for point in points:
            if point in section:
                section = section[point]
            else:
                raise ValueError("This path does not exist!")
        return section
    
    def getBoolean(self, path: str):
        return True if self.get(path) == "True" else False
    
    def getInt(self, path: str):
        return int(self.get(path))
