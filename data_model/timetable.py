from __future__ import annotations
from typing import Optional, List
from data_model.abstract_model import AbstractModel


class TimeTable(AbstractModel):
    """
        object_id - ID данного расписания
        Year - учебный год данного расписания
    """

    def __init__(self, time_table_year: Optional[int] = None,
                 object_id: Optional[int] = None):
        self.__year = time_table_year
        self.__object_id = object_id

    def get_table_id(self) -> Optional[int]:
        return self.__object_id

    def get_year(self) -> Optional[int]:
        return self.__year

    def __str__(self):
        return f"Timetable(object_id={self.__object_id}, year={self.__year})"

    def __dict__(self) -> dict:
        return {"object_id": self.__object_id,
                "time_table_year": self.__year}

    @staticmethod
    def parse(file_timetable: str) -> List[(Optional[str], Optional[TimeTable])]:
        f = open(file_timetable, encoding='utf-8')
        lines = f.read().split('\n')[1:]
        lines = [i.split(';') for i in lines]
        res = []

        for elem in lines:
            try:
                year = int(elem[0])
                res.append((None, TimeTable(time_table_year=year)))
            except (IndexError, ValueError) as error:
                exception_text = f"Запись {lines.index(elem) + 1} строка {lines.index(elem) + 2} " \
                                 f"не добавилась в [res].\nОшибка: {error}"
                print(exception_text)
                res.append((exception_text, None))
            except Exception as error:
                exception_text = f"Неизвестная ошибка в TimeTable.parse():\n{error}"
                print(exception_text + '\n')
                res.append((exception_text, None))
        return res
