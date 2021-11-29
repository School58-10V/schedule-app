from __future__ import annotations
from typing import Optional, List
from data_model.abstract_model import AbstractModel
from data_model.parsed_data import ParsedData



class TeachersOnLessonRows(AbstractModel):
    """
        Класс учителя в LessonRow. Используется для m2m отношения между
        Teacher и LessonRow
                      teacher_id - Идентификационный номер учителя
                   lesson_row_id - Идентификационный номер ряда уроков
        object_id - Идентификационный номер учителя на ряд уроков
    """

    def __init__(self, teacher_id: int, lesson_row_id: int, object_id: Optional[int] = None):
        self.__teacher_id = teacher_id
        self.__lesson_row_id = lesson_row_id
        self._object_id = object_id

    def get_teacher_id(self) -> int:
        return self.__teacher_id

    def get_lesson_row_id(self) -> int:
        return self.__lesson_row_id

    def __str__(self) -> str:
        return f'TeachersOnLessonRows(teacher_id: {self.__teacher_id},' \
               f' lesson_row_id: {self.__lesson_row_id},' \
               f' object_id: {self._object_id})'

    def __dict__(self) -> dict:
        return {"teacher_id": self.__teacher_id,
                "lesson_row_id": self.__lesson_row_id,
                "object_id": self._object_id}

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

                res.append(ParsedData(None, TeachersOnLessonRows(teacher_id=teacher_id, lesson_row_id=lesson_row_id)))
            except (IndexError, ValueError) as error:
                exception_text = f"Запись {lines.index(i) + 1} строка {lines.index(i) + 2} " \
                                 f"не добавилась в [res].\nОшибка: {error}"
                res.append(ParsedData(exception_text, None))
            except Exception as error:
                exception_text = f"Неизвестная ошибка в TeachersOnLessonRows.parse():\n{error}"
                print(exception_text + '\n')
                res.append(ParsedData(exception_text, None))
        return res
