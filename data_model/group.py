from __future__ import annotations  # нужно чтобы parse мог быть типизирован

from data_model.abstract_model import AbstractModel
from typing import Optional, List, TYPE_CHECKING

from data_model.groups_for_students import GroupsForStudents
from data_model.parsed_data import ParsedData
from data_model.student import Student

if TYPE_CHECKING:
    from adapters.file_source import FileSource


class Group(AbstractModel):
    """
        Класс группы.
    """

    def __init__(
            self, db_source: FileSource, teacher_id: int, class_letter: str, grade: int,
            profile_name: str, object_id: Optional[int] = None
            ):
        super().__init__(db_source)
        self.__teacher_id = teacher_id
        self.__class_letter = class_letter
        self.__grade = grade
        self.__profile_name = profile_name  # should be empty if no profile exists
        self._object_id = object_id

    def get_teacher_id(self) -> int:
        return self.__teacher_id

    def get_letter(self) -> str:
        return self.__class_letter

    def get_grade(self) -> int:
        return self.__grade

    def get_profile_name(self) -> str:
        return self.__profile_name

    @staticmethod
    def parse(file_location: str, db_source: FileSource) -> List[(Optional[str], Optional[Group])]:
        with open(file_location, encoding='utf-8') as file:
            lines = file.read().split('\n')[1:]
            lines = [i.split(';') for i in lines]
            res = []
            for i in lines:
                try:
                    teacher_id = i[0]
                    class_letter = i[1]
                    grade = i[2]
                    profile_name = i[3]
                    res.append(ParsedData(None, Group(db_source, int(teacher_id), class_letter,
                                                      int(grade), profile_name)))

                except IndexError as e:
                    exception_text = f"Строка {lines.index(i) + 2} не добавилась в [res]"
                    print(exception_text)
                    print(e)
                    res.append(ParsedData(exception_text, None))
                except Exception as e:
                    exception_text = f"Неизвестная ошибка в Group.parse():\n{e}"
                    print(exception_text)
                    res.append(ParsedData(exception_text, None))
            return res

    def __str__(self) -> str:
        return f'Group(teacher_id={self.__teacher_id}, class_letter={self.__class_letter}, ' \
               f'grade={self.__grade}, profile_name={self.__profile_name}, object_id={self._object_id})'

    def __dict__(self) -> dict:
        return {"teacher_id": self.__teacher_id,
                "class_letter": self.__class_letter,
                "grade": self.__grade,
                "profile_name": self.__profile_name,
                "object_id": self._object_id}

    def get_all_students(self) -> List[Student]:
        """
           Возвращает список объектов GroupsForStudents используя db_source данный в __init__()
           :return: список словарей объектов Student
        """
        return GroupsForStudents.get_student_by_group_id(self._object_id, self._db_source)
