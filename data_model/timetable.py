from __future__ import annotations
from typing import Optional, List
from data_model.abstract_model import AbstractModel


class TimeTable(AbstractModel):
    """
        Table_id - ID данного расписания
        Year - учебный год данного расписания
    """

    def __init__(self, time_table_year: Optional[int] = None,
                 time_table_id: Optional[int] = None):
        self.__year = time_table_year
        self.__table_id = time_table_id

    def get_table_id(self) -> Optional[int]:
        return self.__table_id

    def get_year(self) -> Optional[int]:
        return self.__year

    def __str__(self):
        return f"Timetable(table_id={self.__table_id}, year={self.__year})"

    def __dict__(self) -> dict:
        return {"time_table_id": self.__table_id,
                "time_table_year": self.__year}

    @classmethod
    def get_all(cls, db_path: str = "./db") -> list[TimeTable]:
        data = cls._read_json_db(db_path)
        output = []
        for elem in data:
            output.append(cls(**elem))
        return output

    @classmethod
    def get_by_id(cls, elem_id: int, db_path: str = "./db") -> TimeTable:
        data = cls._read_json_db(db_path)
        for elem in data:
            if elem["time_table_id"] == elem_id:
                return cls(**elem)
        raise ValueError(f"Объект с id {elem_id} не найден")

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

    def get_main_id(self):
        return self.__table_id

    def _set_main_id(self, elem_id: Optional[int] = None):
        self.__table_id = elem_id
