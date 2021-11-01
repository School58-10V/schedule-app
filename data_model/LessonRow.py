# start_time  начальное время
# end_time конечное время
# num_of_group номер группы
# subject_id айди предмета
# room_id айди комнаты
# timetable_id год в который происходят уроки
# lesson_row_id айди самого класса ряд уроков

from __future__ import annotations  # нужно чтобы parse мог быть типизирован
import json

from typing import Optional, List


class LessonRow:
    def __init__(self, start_time: int, end_time: int, group_id: int, subject_id: int, room_id: int,
                 timetable_id: int, lesson_row_id: int = None):
        self.__start_time = start_time  # start time of lessons (9:00)
        self.__end_time = end_time  # end time of lessons (10:00)
        self.__group_id = group_id  # класс, занимающийся в данный момент.(id группы/класса)
        self.__subject_id = subject_id  # Math. Russian language(id)
        self.__room_id = room_id  # id
        self.__timetable_id = timetable_id  # id
        self.__lesson_row_id = lesson_row_id

    def count_studying_hours(self):
        pass

    def get_group_id(self):
        return self.__group_id

    def get_subject_id(self):
        return self.__subject_id

    def get_room_id(self):
        return self.__room_id

    def get_start_time(self):
        return self.__start_time

    def get_end_time(self):
        return self.__end_time

    def get_timetable_id(self):
        return self.__timetable_id

    def get_lesson_row_id(self):
        return self.__lesson_row_id

    @staticmethod
    def parse(file_location) -> List[(Optional[str], Optional[Location])]:
        f = open(file_location, encoding='utf-8')
        lines = f.read().split('\n')[1:]
        lines = [i.split(';') for i in lines]
        res = []

        for i in lines:
            try:
                start_time = i[0]
                end_time = i[1]
                group_id = i[2]
                subject_id = i[3]
                room_id = i[4]
                timetable_id = i[5]
                lesson_row_id = i[6]

                res.append((None, Lesson(start_time, end_time, group_id, subject_id, room_id, timetable_id, lesson_row_id)))
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

    def __str__(self):
        return f'Lesson(day = {self.__day}, start_time = {self.__start_time}, end_time = {self.__end_time}, notes =  {self.__notes}) '

    def __serialize_to_json(self):
        return json.dumps({"start_time": self.__start_time,
                           "end_time": self.__end_time,
                           "group_id": self.__group_id,
                           "subject_id": self.__subject_id,
                           "room_id": self.__room_id,
                           "timetable_id": self.__timetable_id,
                           "lesson_row_id": self.__lesson_row_id}, ensure_ascii=False)

    def save(self, file_way="./db/lessonRows.json"):
        with open(file_way, mode="w", encoding='utf-8') as data_file:
            data_file.write(self.__serialize_to_json())
