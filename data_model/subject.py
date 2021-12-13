from __future__ import annotations
from data_model.teacher import Teacher
from data_model.teachers_for_subjects import TeachersForSubjects
from typing import Optional, List, TYPE_CHECKING
from data_model.abstract_model import AbstractModel
from data_model.parsed_data import ParsedData

if TYPE_CHECKING:
    from adapters.file_source import FileSource


class Subject(AbstractModel):
    """
        name - Название предмета
        object_id - Идентификационный номер предмета
    """

    def __init__(self, db_source: FileSource, subject_name: Optional[str] = None,
                 object_id: Optional[int] = None):
        super().__init__(db_source)
        self.__subject_name = subject_name
        self._object_id = object_id

    def get_subject_name(self) -> str:
        return self.__subject_name

    def get_teachers(self) -> List[Teacher]:
        """
            Ссылается на класс TeachersForSubjects и использует его метод
            :return: список объектов Teacher
        """
        return TeachersForSubjects.get_teachers_by_subject_id(self._object_id, self._db_source)

    @staticmethod
    def parse(file_location: str, db_source: FileSource) -> List[(Optional[str], Optional[Subject])]:
        file = open(file_location, 'r', encoding='utf-8')
        lines = file.read().split('\n')[1:]
        file.close()
        res = []
        for i in lines:
            j = i.split(';')
            try:
                name_subject = j[0]
                res.append(ParsedData(None, Subject(subject_name=name_subject, db_source=db_source)))
            except IndexError as error:
                exception_text = f"Запись {lines.index(i) + 1} строка {lines.index(i) + 2} " \
                                 f"не добавилась в [res].\nОшибка: {error}"
                print(exception_text)
                res.append(ParsedData(exception_text, None))
            except Exception as error:
                exception_text = f"Неизвестная ошибка в Subject.parse():\n{error}"
                print(exception_text + '\n')
                res.append(ParsedData(exception_text, None))
        return res

    def __str__(self):
        return f'Subject(subject_name: {self.__subject_name})'

    def __dict__(self) -> dict:
        return {"object_id": self._object_id,
                "subject_name": self.__subject_name}

