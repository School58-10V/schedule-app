from __future__ import annotations
import json
from typing import Optional, List


class TimeTable:
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
        data = cls.__read_json_db(db_path)
        output = []
        for elem in data:
            output.append(cls(**elem))
        return output

    @classmethod
    def get_by_id(cls, elem_id: int, db_path: str = "./db") -> TimeTable:
        data = cls.__read_json_db(db_path)
        for elem in data:
            if elem["time_table_id"] == elem_id:
                return cls(**elem)
        raise ValueError(f"Объект с id {elem_id} не найден")

    def serialize_to_json(self, indent: Optional[int] = None) -> str:
        return json.dumps(self.__dict__(), ensure_ascii=False, indent=indent)

    @staticmethod
    def __serialize_records_to_json(records: list, indent: Optional[int] = None):
        return json.dumps(records, ensure_ascii=False, indent=indent)

    @classmethod
    def __read_json_db(cls, db_path) -> list:
        try:
            with open(f"{db_path}/{cls.__name__}.json", mode="r", encoding='utf-8') as data_file:
                record = json.loads(data_file.read())
                return record
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return []

    def save(self, output_path: str = './db'):
        current_records = self.__read_json_db(output_path)
        current_records.append(self.__dict__())
        target_json = self.__serialize_records_to_json(current_records)
        with open(f"{output_path}/{type(self).__name__}.json", mode="w", encoding='utf-8') as data_file:
            data_file.write(target_json)

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
