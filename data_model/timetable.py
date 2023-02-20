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
        version - версия расписания
    """

    def __init__(self, db_source: DBSource, time_table_year: Optional[int] = int(datetime.date.today().year),
                 version: Optional[int] = None, object_id: Optional[int] = None):
        super().__init__(db_source)
        self.__year = time_table_year
        self._version = version
        self._object_id = object_id

    def get_year(self) -> Optional[int]:
        return self.__year

    def get_version(self) -> Optional[int]:
        return self._version

    def __str__(self):
        return f"Timetable(year={self.get_year()}, version={self.get_version()})"

    def __dict__(self) -> dict:
        return {"object_id": self.get_main_id(),
                "time_table_year": self.get_year(),
                "version": self.get_version()}

    @classmethod
    def get_current_timetable(cls, db_source: AbstractSource):
        try:
            return sorted([cls(db_source, **timetable_in_dct) for timetable_in_dct in db_source.get_by_query(cls._get_collection_name(), {'time_table_year': datetime.date.today().year})], key=lambda x: x.get_version())[-1]
        except IndexError:
            raise ValueError('На этот год нет расписания.')

    @classmethod
    def get_by_year(cls, year: int, db_source: AbstractSource) -> TimeTable:
        try:
            return sorted([cls(db_source, **timetable_in_dct) for timetable_in_dct in db_source.get_by_query(cls._get_collection_name(), {'time_table_year': year})], key=lambda x: x.get_version())[-1]
        except IndexError:
            raise ValueError('На этот год нет расписания.')

    @classmethod
    def get_all_by_year(cls, year: int, db_source: AbstractSource) -> list[TimeTable]:
        try:
            return [cls(db_source, **timetable_in_dct) for timetable_in_dct in
                        db_source.get_by_query(cls._get_collection_name(), {'time_table_year': year, 'version' : version})][0]
        except IndexError:
            raise ValueError('Такого расписания не существует.')

    @classmethod
    def get_by_version_and_year(cls, year: int, version: int, db_source: AbstractSource):
        return [cls(db_source, **timetable_in_dct) for timetable_in_dct in
                db_source.get_by_query(cls._get_collection_name(), {'time_table_year': year})]

    @staticmethod
    def parse(file_timetable: str, db_source: DBSource) -> List[(Optional[str], Optional[TimeTable])]:
        f = open(file_timetable, encoding='utf-8')
        lines = f.read().split('\n')[1:]
        lines = [i.split(';') for i in lines]
        res = []

        for elem in lines:
            try:
                year = int(elem[0])
                version = int(elem[1])
                res.append(ParsedData(None, TimeTable(time_table_year=year, version=version, db_source=db_source)))
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

    # не знаю, какой модификатор доступа сюда вставить
    def save(self):
        if self.get_version() is None:
            if self._db_source.get_by_query(self._get_collection_name(), {'time_table_year': self.get_year()}):
                self._set_version(self.get_by_year(self.get_year(), self._db_source).get_version() + 1)
            else:
                self._set_version(1)
        super(self.__class__, self).save()
        return self

    def _set_version(self, version):
        self._version = version
        return self