from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING
from data_model.abstract_model import AbstractModel
from data_model.parsed_data import ParsedData

if TYPE_CHECKING:
    from adapters.file_source import FileSource


class TimeTable(AbstractModel):
    """
        object_id - ID данного расписания
        Year - учебный год данного расписания
    """

    def __init__(self, db_source: FileSource, time_table_year: Optional[int] = None,
                 object_id: Optional[int] = None):
        super().__init__(db_source)
        self.__year = time_table_year
        self._object_id = object_id

    def get_year(self) -> Optional[int]:
        return self.__year

    def __str__(self):
        return f"Timetable(object_id={self.get_main_id()}, year={self.get_year})"

    def __dict__(self) -> dict:
        return {"object_id": self.get_main_id(),
                "time_table_year": self.get_year()}

    @staticmethod
    def parse(file_timetable: str, db_source: FileSource) -> List[(Optional[str], Optional[TimeTable])]:
        f = open(file_timetable, encoding='utf-8')
        lines = f.read().split('\n')[1:]
        lines = [i.split(';') for i in lines]
        res = []

        for elem in lines:
            try:
                year = int(elem[0])
                res.append(ParsedData(None, TimeTable(time_table_year=year, db_source=db_source)))
            except (IndexError, ValueError) as error:
                exception_text = f"Запись {lines.index(elem) + 1} строка {lines.index(elem) + 2} " \
                                 f"не добавилась в [res].\nОшибка: {error}"
                print(exception_text)
                res.append(ParsedData(exception_text, None))
            except Exception as error:
                exception_text = f"Неизвестная ошибка в TimeTable.parse():\n{error}"
                print(exception_text + '\n')
                res.append(ParsedData(exception_text, None))
        return res
