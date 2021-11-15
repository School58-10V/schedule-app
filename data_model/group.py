from __future__ import annotations  # нужно чтобы parse мог быть типизирован

from data_model.abstract_model import AbstractModel
from typing import Optional, List


class Group(AbstractModel):
    """
        Класс группы.
    """

    def __init__(
            self, teacher_id: int, class_letter: str, grade: int,
            profile_name: str, group_id: Optional[int] = None
            ):
        self.__teacher_id = teacher_id
        self.__class_letter = class_letter
        self.__grade = grade
        self.__profile_name = profile_name  # should be empty if no profile exists
        self.__group_id = group_id

    def get_teacher_id(self) -> int:
        return self.__teacher_id

    def get_letter(self) -> str:
        return self.__class_letter

    def get_grade(self) -> int:
        return self.__grade

    def get_profile_name(self) -> str:
        return self.__profile_name

    def get_id(self) -> Optional[int]:
        return self.__group_id

    @classmethod
    def get_all(cls, db_path: str = "./db") -> List[Group]:
        return [cls(**i) for i in cls._read_json_db(db_path)]

    @classmethod
    def get_by_id(cls, element_id: int, db_path: str = "./db") -> Group:
        for i in cls._read_json_db(db_path):
            if i['group_id'] == element_id:
                return cls(**i)
        raise ValueError(f"Объект с id {element_id} не найден")

    @staticmethod
    def parse(file_location: str) -> List[(Optional[str], Optional[Group])]:
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
                    group_id = i[4]
                    res.append((None, Group(int(teacher_id), class_letter, int(grade), profile_name, int(group_id))))

                except IndexError as e:
                    exception_text = f"Строка {lines.index(i) + 2} не добавилась в [res]"
                    print(exception_text)
                    print(e)
                    res.append((exception_text, None))
                except Exception as e:
                    exception_text = f"Неизвестная ошибка в Group.parse():\n{e}"
                    print(exception_text)
                    res.append((exception_text, None))
            return res

    def __str__(self) -> str:
        return f'Group(teacher_id={self.__teacher_id}, class_letter={self.__class_letter}, ' \
               f'grade={self.__grade}, profile_name={self.__profile_name}, group_id={self.__group_id})'

    def __dict__(self) -> dict:
        return {"teacher_id": self.__teacher_id,
                "class_letter": self.__class_letter,
                "grade": self.__grade,
                "profile_name": self.__profile_name,
                "group_id": self.__group_id}

    def get_main_id(self):
        return self.__group_id

    def _set_main_id(self, elem_id: Optional[int] = None):
        self.__group_id = elem_id
