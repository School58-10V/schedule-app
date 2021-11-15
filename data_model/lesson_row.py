
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
        self.__start_time = start_time
        self.__end_time = end_time
        self.__group_id = group_id
        self.__subject_id = subject_id
        self.__room_id = room_id
        self.__timetable_id = timetable_id
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

    def __dict__(self) -> dict:
        return {
            "count_studying_hours": self.__count_studying_hours,
            "group_id": self.__group_id,
            "subject_id": self.__subject_id,
            "room_id": self.__room_id,
            "start_time": self.__start_time,
            "end_time": self.__end_time,
            "timetable_id": self.__timetable_id,
            "lesson_row_id": self.__lesson_row_id
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
        return f'LessonRow(count_studying_hours={self.__count_studying_hours}, group_id={self.__group_id}, ' \
               f'subject_id={self.__subject_id} ' \
               f'room_id={self.__room_id}), start_time={self.__start_time}), end_time={self.__end_time}), ' \
               f'timetable_id={self.__timetable_id}), ' \
               f'lesson_row_id={self.__lesson_row_id}) '

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
                lesson_row_id = i[7]

                res.append((None, LessonRow(int(count_studying_hours), int(group_id), int(subject_id), int(room_id),
                                            int(start_time), int(end_time), int(timetable_id),
                                            int(lesson_row_id))))
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

    @classmethod
    def get_all(cls, db_path: str = "../db") -> list[LessonRow]:
        list_of_objects = cls.__read_json_db(db_path)
        return [cls(count_studying_hours=cnt['count_studying_hours'], group_id=cnt["group_id"],
                    subject_id=cnt["subject_id"], room_id=cnt["room_id"], start_time=cnt["start_time"],
                    end_time=cnt["end_time"], lesson_row_id=cnt["lesson_row_id"], timetable_id=cnt["timetable_id"])
                for cnt in list_of_objects]

    @classmethod
    def get_by_id(cls, element_id: int, db_path: str = "../db") -> LessonRow:
        for i in cls.__read_json_db(db_path):
            if i['lesson_row_id'] == element_id:
                return cls(**i)
        raise ValueError(f"Объект с id {element_id} не найден")