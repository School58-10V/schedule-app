from __future__ import annotations

from abc import ABC, abstractmethod


class AbstractValidator(ABC):
    def __init__(self, required_keys: set, allowed_keys: set, keys_types: dict):
        self.required_keys = required_keys
        self.allowed_keys = allowed_keys
        self.keys_types = keys_types

    def validate(self, request: dict, method: str):
        if method == 'PUT':
            self.required_keys.add('object_id')
            self.allowed_keys.add('object_id')

        for key in self.required_keys:
            if key not in request.keys():
                raise ValueError

        for key in request.keys():
            if key not in self.allowed_keys:
                raise ValueError
            if type(self.keys_types[key]) == str:  # обработка случая list[int] и т.п
                value = self.keys_types[key].split('[')[1][:-1]
                if type(request[key]) != list or not self.check_list_items(request[key], eval(value)):
                    raise ValueError

            if type(request[key]) != self.keys_types[key]:
                raise ValueError

    @staticmethod
    def check_list_items(arr: list, value: type) -> bool:
        for elem in arr:
            if type(elem) != value:
                return False
        return True

    @staticmethod
    @abstractmethod
    def get_name():
        pass
