# start_time  начальное время
# end_time конечное время
# num_of_group номер группы
# subject_id айди предмета
# room_id айди комнаты
# timetable_id год в который происходят уроки
# lesson_row_id айди самого класса ряд уроков

from __future__ import annotations

import json

from typing import Optional, List


class LessonRow:
    def __init__(self, group_id: int, subject_id: int, room_id: int, start_time: int, end_time: int,
                 timetable_id: int, lesson_row_id: int = None):
        self.__count_studying_hours = None
        self.__start_time = start_time  # start time of lessons (9:00)
        self.__end_time = end_time  # end time of lessons (10:00)
        self.__group_id = group_id  # класс, занимающийся в данный момент.(id группы/класса)
        self.__subject_id = subject_id  # Math. Russian language(id)
        self.__room_id = room_id  # id
        self.__timetable_id = timetable_id  # id
        self.__lesson_row_id = lesson_row_id

    def count_studying_hours(self):
        pass

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

    def get_lesson_row_id(self) -> int:
        return self.__lesson_row_id

    def __serialize_to_json(self):
        return json.dumps({"count_studying_hours": self.__count_studying_hours,
                           "group_id": self.__group_id,
                           "subject_id": self.__subject_id,
                           "room_id": self.__room_id,
                           "start_time": self.__start_time,
                           "end_time": self.__end_time,
                           "timetable_id": self.__timetable_id,
                           "lesson_row_id": self.__lesson_row_id}, ensure_ascii=False)

    def save(self, path="./db/lesson_row.json"):
        with open(path, mode="w", encoding='utf-8') as data_file:
            data_file.write(self.__serialize_to_json())

    def __str__(self):
        return f'LessonRow(count_studying_hours={self.__count_studying_hours}, group_id={self.__group_id}, subject_id={self.__subject_id} ' \
               f'room_id={self.__room_id}), start_time={self.__start_time}, end_time={self.__end_time}), timetable_id={self.__timetable_id}), '

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

                res.append((None, LessonRow(int(count_studying_hours), int(group_id), int(subject_id), int(room_id), int(start_time),
                                            int(end_time), int(timetable_id))))

            except IndexError as e:
                exception_text = f"Строка {lines.index(i) + 2} не добавилась в [res]"
                print(exception_text)
                print(e)
                res.append((exception_text, None))
            except Exception as e:
                exception_text = f"Неизвестная ошибка в LessonRow.parse():\n{e}"
                print(exception_text)
                res.append((exception_text, None))
        return res
