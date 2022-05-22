from __future__ import annotations

from abc import ABC, abstractmethod


class AbstractValidator(ABC):

    @abstractmethod
    def validate(self, request: dict, method: str):
        pass

    @staticmethod
    @abstractmethod
    def get_name():
        pass
