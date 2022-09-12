from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from adapters.db_source import DBSource


class TestClass:
    def __init__(self, db_source: DBSource):
        self.__db_source = db_source

    def get_db_source(self) -> DBSource:
        return self.__db_source

    def __get_subject(self):
        pass

    def run(self, num1, num2, num3):
        pass
