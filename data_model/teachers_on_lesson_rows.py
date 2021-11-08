from __future__ import annotations
import json
from typing import Optional, List


class TeachersOnLessonRows:
    """
        Класс учителя в LessonRow. Используется для m2m отношения между
        Teacher и LessonRow
                      teacher_id - Идентификационный номер учителя
                   lesson_row_id - Идентификационный номер ряда уроков
        teacher_on_lesson_row_id - Идентификационный номер учителя на ряд уроков
    """

    def __init__(self, teacher_id: int, lesson_row_id: int, teacher_on_lesson_row_id: Optional[int] = None):
        self.__teacher_id = teacher_id
        self.__lesson_row_id = lesson_row_id
        self.__teacher_on_lesson_row_id = teacher_on_lesson_row_id

    def get_teacher_id(self) -> int:
        return self.__teacher_id

    def get_lesson_row_id(self) -> int:
        return self.__lesson_row_id

    def get_teacher_on_lesson_row_id(self) -> Optional[int]:
        return self.__teacher_on_lesson_row_id

    def __str__(self) -> str:
        return f'TeachersOnLessonRows(teacher_id: {self.__teacher_id},' \
               f' lesson_row_id: {self.__lesson_row_id},' \
               f' teacher_on_lesson_row_id: {self.__teacher_on_lesson_row_id})'

    def __serialize_to_json(self, indent: int = None) -> str:
        return json.dumps(self.__dict__(), ensure_ascii=False, indent=indent)

    def __dict__(self) -> dict:
        return {"teacher_id": self.__teacher_id,
                "lesson_row_id": self.__lesson_row_id,
                "teacher_on_lesson_row_id": self.__teacher_on_lesson_row_id}

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

    def save(self, output_path: str = './db'):
        current_records = self.__read_json_db(output_path)
        current_records.append(self.__dict__())
        target_json = self.__class__.serialize_records_to_json(current_records)
        with open(f"{output_path}/{type(self).__name__}.json", mode="w", encoding='utf-8') as data_file:
            data_file.write(target_json)

    @staticmethod
    def parse(file_location: str) -> List[(Optional[str], Optional[TeachersOnLessonRows])]:
        file = open(file_location, 'r', encoding='utf-8')
        lines = file.read().split('\n')[1:]
        file.close()
        res = []
        for i in lines:
            j = i.split(';')
            try:
                teacher_id = int(j[0])
                lesson_row_id = int(j[1])
                # teacher_on_lesson_row_id = int(j[2])

                res.append((None, TeachersOnLessonRows(teacher_id=teacher_id, lesson_row_id=lesson_row_id)))
            except (IndexError, ValueError) as error:
                exception_text = f"Запись {lines.index(i) + 1} строка {lines.index(i) + 2} " \
                                 f"не добавилась в [res].\nОшибка: {error}"
                res.append((exception_text, None))
            except Exception as error:
                exception_text = f"Неизвестная ошибка в TeachersOnLessonRows.parse():\n{error}"
                print(exception_text + '\n')
                res.append((exception_text, None))
        return res
