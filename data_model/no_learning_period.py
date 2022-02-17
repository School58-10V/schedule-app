from __future__ import annotations
from data_model.parsed_data import ParsedData
from data_model.abstract_model import AbstractModel
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from adapters.db_source import DBSource


class NoLearningPeriod(AbstractModel):
    def __init__(self, db_source: DBSource, start: str, stop: str, timetable_id: int,
                 object_id: Optional[int] = None):
        # start и stop указаны как DATE в POSTGRES DB!!!
        """
            timetable_id - id расписания
            start - начало каникул
            stop - конец каникул
            object_id - id каникул
        """
        super().__init__(db_source)
        self._object_id = object_id
        self.__start_time = start
        self.__stop_time = stop
        self.__timetable_id = timetable_id

    def get_start_time(self) -> str:
        return self.__start_time

    def get_stop_time(self) -> str:
        return self.__stop_time

    def get_timetable_id(self) -> int:
        return self.__timetable_id

    def __dict__(self) -> dict:
        return {
            "timetable_id": self.get_timetable_id(),
            "start": self.get_start_time(),
            "stop": self.get_stop_time(),
            "object_id": self.get_main_id()
        }

    def __str__(self):
        return f'NoLearningPeriod(timetable_id={self.get_timetable_id()}, start={self.get_start_time()}, ' \
               f'stop={self.get_stop_time()}, object_id={self.get_main_id()})'

    @staticmethod
    def parse(file_no_learning_period, db_source: DBSource) -> List[(Optional[str], Optional[NoLearningPeriod])]:
        f = open(file_no_learning_period, encoding='utf-8')
        lines = f.read().split('\n')[1:]
        lines = [i.split(';') for i in lines]
        res = []
        for i in lines:
            try:
                start = i[0]
                stop = i[1]
                res.append(ParsedData(None, NoLearningPeriod(start=start, stop=stop, db_source=db_source)))
            except IndexError as e:
                exception_text = f"Строка {lines.index(i) + 2} не добавилась в [res]"
                print(exception_text)
                print(e)
                res.append(ParsedData(exception_text, None))
            except Exception as e:
                exception_text = f"Неизвестная ошибка в NoLearningPeriod.parse():\n{e}"
                print(exception_text)
                res.append(ParsedData(exception_text, None))
        return res
