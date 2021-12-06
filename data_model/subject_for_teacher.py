from __future__ import annotations
from data_model.abstract_model import AbstractModel
from typing import List, Optional, TYPE_CHECKING
from data_model.parsed_data import ParsedData

if TYPE_CHECKING:
    from adapters.file_source import FileSource


class SubjectForTeacher(AbstractModel):
    """
    Вспомогательный класс для реализации связей many to many между Teacher и Student
    """

    def __init__(self, db_source: FileSource, teacher_id: int, subject_id: int, object_id: Optional[int] = None):
        """
    :param teacher_id - Идентификационный номер Teacher
    :param subject_id - Идентификационный номер Subject
    :param object_id - Идентификационный номер Student_for_teacher(опционально)

    """

        super().__init__(db_source)
        self.__teacher_id = teacher_id
        self.__subject_id = subject_id
        self.__object_id = object_id

    def get_teacher_id(self) -> int:
        return self.__teacher_id

    def get_subject_id(self) -> int:
        return self.__subject_id

