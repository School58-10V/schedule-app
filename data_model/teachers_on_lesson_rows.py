from __future__ import annotations
from typing import Optional, List
from data_model.abstract_model import AbstractModel


class TeachersOnLessonRows(AbstractModel):
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

    def __dict__(self) -> dict:
        return {"teacher_id": self.__teacher_id,
                "lesson_row_id": self.__lesson_row_id,
                "teacher_on_lesson_row_id": self.__teacher_on_lesson_row_id}

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

    @classmethod
    def get_all(cls, db_path: str = "./db") -> list[TeachersOnLessonRows]:
        data = cls._read_json_db(db_path)
        return [cls(**i) for i in data]

    @classmethod
    def get_by_id(cls, teacher_on_lesson_row_id: int, db_path: str = "./db") -> TeachersOnLessonRows:
        data = cls._read_json_db(db_path)
        for i in data:
            if i["teacher_on_lesson_row_id"] == teacher_on_lesson_row_id:
                return cls(**i)
        raise ValueError(f"Объект с id {teacher_on_lesson_row_id} не найден")

    def get_main_id(self):
        return self.__teacher_on_lesson_row_id

    def _set_main_id(self, elem_id: Optional[int] = None):
        self.__teacher_on_lesson_row_id = elem_id
