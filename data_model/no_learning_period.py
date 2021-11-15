##          timetable_id - id расписания
##                 start - начало каникул
##                  stop - конец каникул
## no_learning_period_id - id каникул


import json
from datetime import date
from typing import List, Optional
from __future__ import annotations


class NoLearningPeriod:
    def __init__(self, timetable_id: int, start: date, stop: date,
                 no_learning_period_id: int = None):
        # Для начала и конца каникул можно использовать только дату
        self.__no_learning_period_id = no_learning_period_id
        self.__start_time = start
        self.__stop_time = stop
        self.__timetable_id = timetable_id

    def get_no_learning_period_id(self) -> int:
        return self.__no_learning_period_id

    def get_star_time(self) -> date:
        return self.__start_time

    def get_stop_time(self) -> date:
        return self.__stop_time

    def get_timetable_id(self) -> int:
        return self.__timetable_id

    def __dict__(self) -> dict:
        return {
            "timetable_id": self.__timetable_id,
            "start": self.__start_time,
            "stop": self.__stop_time,
            "no_learning_period_id": self.__no_learning_period_id
        }

    def serialize_to_json(self, indent: int = None) -> str:
        return json.dumps(self.__dict__(), ensure_ascii=False, indent=indent)

    @staticmethod
    def serialize_records_to_json(records: list, indent: int = None) -> str:
        return json.dumps(records, ensure_ascii=False, indent=indent)

    @classmethod
    def __read_json_db(cls, db_path) -> list:
        try:
            with open(f"{db_path}/{cls.__name__}.json",
                      mode="r", encoding='utf-8') as data_file:
                record = json.loads(data_file.read())
                return record
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return []

    def save(self, output_path: str = '../db'):
        current_records = self.__read_json_db(output_path)
        current_records.append(self.__dict__())
        target_json = self.__class__.serialize_records_to_json(current_records)
        with open(f"{output_path}/{type(self).__name__}.json", mode="w", encoding='utf-8') as data_file:
            data_file.write(target_json)

    def __str__(self):
        return f'NoLearningPeriod(timetable_id={self.__timetable_id}, start={self.__start_time}, ' \
               f'stop={self.__stop_time}, no_learning_period_id={self.__no_learning_period_id})'

    @staticmethod
    def parse(file_no_learning_period) -> List[(Optional[str], Optional[NoLearningPeriod])]:
        f = open(file_no_learning_period, encoding='utf-8')
        lines = f.read().split('\n')[1:]
        lines = [i.split(';') for i in lines]
        res = []
        for i in lines:
            try:
                start = i[1]
                stop = i[2]
                res.append((None, NoLearningPeriod(int(timetable_id), start, stop, no_learning_period_id)))
            except IndexError as e:
                exception_text = f"Строка {lines.index(i) + 2} не добавилась в [res]"
                print(exception_text)
                print(e)
                res.append((exception_text, None))
            except Exception as e:
                exception_text = f"Неизвестная ошибка в NoLearningPeriod.parse():\n{e}"
                print(exception_text)
                res.append((exception_text, None))
        return res

    @classmethod
    def get_all(cls, db_path: str = "../db") -> list[NoLearningPeriod]:
        list_of_objects = cls.__read_json_db(db_path)
        return [cls(timetable_id=cnt['timetable_id'], start=cnt["start"],
                    stop=cnt["stop"], no_learning_period_id=cnt["no_learning_period_id"]) for cnt in list_of_objects]

    @classmethod
    def get_by_id(cls, element_id: int, db_path: str = "../db") -> NoLearningPeriod:
        for i in cls.__read_json_db(db_path):
            if i['no_learning_period_id'] == element_id:
                return cls(**i)
        raise ValueError(f"Объект с id {element_id} не найден")