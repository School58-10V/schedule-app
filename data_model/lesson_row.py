from __future__ import annotations
from data_model.abstract_model import AbstractModel
from typing import Optional, List
from data_model.parsed_data import ParsedData


class LessonRow(AbstractModel):
    def __init__(self, count_studying_hours: int, group_id: int, subject_id: int, room_id: int, start_time: int,
                 end_time: int, timetable_id: int, object_id: Optional[int] = None):
        self.__count_studying_hours = count_studying_hours
        self.__start_time = start_time
        self.__end_time = end_time
        self.__group_id = group_id
        self.__subject_id = subject_id
        self.__room_id = room_id
        self.__timetable_id = timetable_id
        self._object_id = object_id

    """
        start_time  начальное время
        end_time конечное время
        num_of_group номер группы
        subject_id айди предмета
        room_id айди комнаты
        timetable_id год в который происходят уроки
        object_id айди самого класса ряд уроков
    """

    def get_group_id(self) -> int:
        return self.__group_id

    def get_subject_id(self) -> int:
        return self.__subject_id

    def get_room_id(self) -> int:
        return self.__room_id

    def get_start_time(self) -> int:
        return self.__start_time

    def get_end_time(self) -> int:
        return self.__end_time

    def get_timetable_id(self) -> int:
        return self.__timetable_id

    def __dict__(self) -> dict:
        return {
            "count_studying_hours": self.__count_studying_hours,
            "group_id": self.__group_id,
            "subject_id": self.__subject_id,
            "room_id": self.__room_id,
            "start_time": self.__start_time,
            "end_time": self.__end_time,
            "timetable_id": self.__timetable_id,
            "object_id": self._object_id}

    def __str__(self):
        return f'LessonRow(count_studying_hours={self.__count_studying_hours}, group_id={self.__group_id}' \
               f', subject_id={self.__subject_id}, room_id={self.__room_id}), start_time={self.__start_time})' \
               f', end_time={self.__end_time}), timetable_id={self.__timetable_id})' \
               f', object_id={self._object_id}) '

    @staticmethod
    def parse(file_location) -> List[(Optional[str], Optional[LessonRow])]:
        f = open(file_location, encoding='utf-8')
        lines = f.read().split('\n')[1:]
        lines = [i.split(';') for i in lines]
        res = []
        for i in lines:
            try:
                count_studying_hours = i[0]
                group_id = i[1]
                subject_id = i[2]
                room_id = i[3]
                start_time = i[4]
                end_time = i[5]
                timetable_id = i[6]

                res.append(ParsedData(None, LessonRow(int(count_studying_hours), int(group_id), int(subject_id),
                                                      int(room_id), int(start_time), int(end_time), int(timetable_id))))
            except IndexError as e:
                exception_text = f"Строка {lines.index(i) + 2} не добавилась в [res]"
                print(exception_text)
                print(e)
                res.append(ParsedData(exception_text, None))
            except Exception as e:
                exception_text = f"Неизвестная ошибка в LessonRow.parse():\n{e}"
                print(exception_text)
                res.append(ParsedData(exception_text, None))
        return res
