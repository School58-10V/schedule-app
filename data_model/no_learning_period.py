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

    def __serialize_to_json(self):
        return json.dumps({"timetable_id": self.__timetable_id,
                       "start": self.__start_time,
                       "stop": self.__stop_time,
                       "no_learning_period_id": self.__no_learning_period_id}, ensure_ascii=False)

    def save(self, path="./db/no_learning_periods.json"):
        with open(path, mode="w", encoding='utf-8') as data_file:
            data_file.write(self.__serialize_to_json())

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
                timetable_id = i[0]
                start = i[1]
                stop = i[2]
                no_learning_period_id = i[3]
                res.append((None, NoLearningPeriod(timetable_id, start, stop, no_learning_period_id)))
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
