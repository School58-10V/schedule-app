from __future__ import annotations

import datetime
from typing import Optional, List, TYPE_CHECKING

from adapters.abstract_source import AbstractSource
from data_model.abstract_model import AbstractModel
from data_model.parsed_data import ParsedData

if TYPE_CHECKING:
    from adapters.db_source import DBSource


class TimeTable(AbstractModel):
    """
        object_id - ID данного расписания
        Year - учебный год данного расписания
    """

    def __init__(self, db_source: DBSource, time_table_year: Optional[int] = None,
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

    @classmethod
    def get_by_year(cls, year: int, db_source: AbstractSource) -> TimeTable:
        try:
            return cls(db_source, **(db_source.get_by_query(cls._get_collection_name(), {'time_table_year': year})[0]))
        except IndexError:
            raise ValueError('ВНИМАНИЕ! У НАС 2 ОБЪЕКТА TIMETABLE С ОДИНАКОВЫМ ГОДОМ, ТАКОГО БЫТЬ НЕ ДОЛЖНО!!!')

    @staticmethod
    def parse(file_timetable: str, db_source: DBSource) -> List[(Optional[str], Optional[TimeTable])]:
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

    @classmethod
    def get_by_current_year(cls, db_source: DBSource, year: int = datetime.date.today().year) -> TimeTable:
        # Метод, который дает объект расписания по году
        return [TimeTable.get_by_id(i['object_id'], db_source)
                for i in db_source.get_by_query(cls._get_collection_name(), {'time_table_year': year})][0]
