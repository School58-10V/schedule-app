from __future__ import annotations  # нужно чтобы parse мог быть типизирован

import json
from typing import List, Optional


class Lesson:
    """
        Класс урока
        start_time начало урока
        end_time конец урока
        day дата
        teacher_id замена
        group_id группа учеников
        subject_id предмет
        notes примечания
        lesson_id урок
        state состояние
    """

    def __init__(self, start_time: int, end_time: int, day: int, teacher_id: int, group_id: int,
                 subject_id: int, notes: str, lesson_id: int = None, state: bool = True):
        self.__start_time = start_time
        self.__end_time = end_time
        self.__day = day
        self.__teacher_id = teacher_id
        self.__group_id = group_id
        self.__subject_id = subject_id
        self.__notes = notes
        self.__lesson_id = lesson_id
        self.__state = state

    def toggle_state(self):
        self.__state = not self.__state

    # get functions

    def get_start_time(self) -> int:
        return self.__start_time

    def get_end_time(self) -> int:
        return self.__end_time

    def get_day(self) -> int:
        return self.__day

    def get_teacher_id(self) -> int:
        return self.__teacher_id

    def get_group_id(self) -> int:
        return self.__group_id

    def get_subject_id(self) -> int:
        return self.__subject_id

    def get_notes(self) -> str:
        return self.__notes

    def get_lesson_id(self) -> int:
        return self.__lesson_id

    def get_state(self) -> bool:
        return self.__state

    def __str__(self):
        return f"Урок с id={self.__lesson_id}"

    @classmethod
    def __read_json_db(cls, db_path) -> list:
        try:
            with open(f"{db_path}/{cls.__name__}.json", mode="r", encoding='utf-8') as data_file:
                record = json.loads(data_file.read())
                return record
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return []

    def __serialize_to_json(self, records: list, indent: Optional[int] = None) -> str:
        records.append({"start_time": self.__start_time,
                        "end_time": self.__end_time,
                        "day": self.__day,
                        "teacher_id": self.__teacher_id,
                        "group_id": self.__group_id,
                        "subject_id": self.__subject_id,
                        "notes": self.__notes,
                        "lesson_id": self.__lesson_id,
                        "state": self.__state})
        return json.dumps(records, ensure_ascii=False, indent=indent)

    @staticmethod
    def parse(file_location: str) -> List[(Optional[str], Optional[Lesson])]:
        with open(file_location, encoding='utf-8') as file:
            lines = file.read().split('\n')[1:]
            lines = [i.split(';') for i in lines]
            res = []
            for i in lines:
                try:
                    start_time = i[0]
                    end_time = i[1]
                    day = i[2]
                    teacher_id = i[3]
                    group_id = i[4]
                    subject_id = i[5]
                    notes = i[6]
                    lesson_id = i[7]
                    state = i[8] == 'True'
                    res.append((None, Lesson(int(start_time), int(end_time), int(day), int(teacher_id),
                                             int(group_id), int(subject_id), notes, int(lesson_id), state)))

                except IndexError as e:
                    exception_text = f"Строка {lines.index(i) + 2} не добавилась в [res]"
                    print(exception_text)
                    print(e)
                    res.append((exception_text, None))
                except Exception as e:
                    exception_text = f"Неизвестная ошибка в Lesson.parse():\n{e}"
                    print(exception_text)
                    res.append((exception_text, None))
            return res

    def save(self, output_path: str = './db'):
        current_records = self.__read_json_db(output_path)
        target_json = self.__serialize_to_json(current_records)
        with open(f"{output_path}/{type(self).__name__}.json", mode="w", encoding='utf-8') as data_file:
            data_file.write(target_json)
