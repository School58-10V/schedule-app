from __future__ import annotations
from data_model.abstract_model import AbstractModel
from typing import List, Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from data_model.teacher import Teacher
    from adapters.file_source import FileSource


class TeachersForSubjects(AbstractModel):
    """
        Вспомогательный класс для реализации связей many to many между Subject и Teacher
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
        return f'TeachersForSubjects(teacher_id: {self.get_teacher_id()},' \
               f' subject_id: {self.get_subject_id()},' \
               f' object_id: {self.get_main_id()})'

    def __dict__(self):
        return {"teacher_id": self.get_teacher_id(),
                "subject_id": self.get_subject_id(),
                "object_id": self.get_main_id()}

    @classmethod
    def _get_collection_name(cls):
        return "SubjectsAndTeachers"

    @classmethod
    def get_teachers_by_subject_id(cls, subject_id: int, db_source: FileSource) -> List[Teacher]:
        # в качестве аргумента подаем id, по которому будем искать все Teacher
        from data_model.teacher import Teacher
        return [Teacher.get_by_id(i["teacher_id"], db_source) for i in
                db_source.get_by_query(cls._get_collection_name(), query={"subject_id": subject_id})]
        # используя метод get_by_query достаем "SubjectsAndTeachers", в описании которых ключ "subject_id" соответствует
        # subject_id в вводимом аргументе. Из полученного списка словарей достаем из каждого словаря
        # по ключу "subject_id" его id и передаем в метод, вызываемой от класса Teacher

