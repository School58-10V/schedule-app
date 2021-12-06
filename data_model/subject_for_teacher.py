from __future__ import annotations
from data_model.abstract_model import AbstractModel
from typing import List, Optional, TYPE_CHECKING
from data_model.parsed_data import ParsedData

if TYPE_CHECKING:
    from adapters.file_source import FileSource


class SubjectForTeacher(AbstractModel):
    """
    Вспомогательный класс для реализации связей many to many между Teacher и Subject
    """

    def __init__(self, db_source: FileSource, teacher_id: int, subject_id: int, object_id: Optional[int] = None):
        """
    :param teacher_id - Идентификационный номер Teacher
    :param subject_id - Идентификационный номер Subject
    :param object_id - Идентификационный номер SubjectForTeacher(опционально)

    """

        super().__init__(db_source)
        self.__teacher_id = teacher_id
        self.__subject_id = subject_id
        self._object_id = object_id

    def get_teacher_id(self) -> int:
        return self.__teacher_id

    def get_subject_id(self) -> int:
        return self.__subject_id

    def __str__(self):
        return f'SubjectForTeacher(teacher_id: {self.__teacher_id},' \
               f' subject_id: {self.__subject_id},' \
               f' object_id: {self._object_id})'

    def __dict__(self):
        return {"teacher_id": self.__teacher_id,
                "subject_id": self.__subject_id,
                "object_id": self._object_id}

    @staticmethod
    def parse(file_location: str) -> List[(Optional[str], Optional[SubjectForTeacher])]:
        file = open(file_location, 'r', encoding='utf-8')
        lines = file.read().split('\n')[1:]
        file.close()
        res = []
        for i in lines:
            j = i.split(';')
            try:
                teacher_id = int(j[0])
                subject_id = int(j[1])

                res.append(ParsedData(None, SubjectForTeacher(teacher_id=teacher_id, subject_id=subject_id)))  # надо добавить db_source
            except (IndexError, ValueError) as error:
                exception_text = f"Запись {lines.index(i) + 1} строка {lines.index(i) + 2} " \
                                 f"не добавилась в [res].\nОшибка: {error}"
                res.append(ParsedData(exception_text, None))
            except Exception as error:
                exception_text = f"Неизвестная ошибка в SubjectForTeacher.parse():\n{error}"
                print(exception_text + '\n')
                res.append(ParsedData(exception_text, None))
        return res
