from __future__ import annotations  # нужно чтобы parse мог быть типизирован

from typing import Optional, List

from data_model.abstract_model import AbstractModel


class StudentInGroup(AbstractModel):
    """
        Класс ученика в группе. Используется для m2m отношения между
        Group и Student
        student_id - айди ученика
        group_id - айди группы
        object_id - айди группы учeников
    """

    def __init__(self, student_id: int, group_id: int, object_id: Optional[int] = None):
        self.__student_id = student_id
        self.__group_id = group_id
        self._object_id = object_id

    def get_student_id(self) -> int:
        return self.__student_id

    def get_group_id(self) -> int:
        return self.__group_id

    @staticmethod
    def parse(file_location) -> List[(Optional[str], Optional[StudentInGroup])]:
        f = open(file_location, encoding='utf-8')
        lines = f.read().split('\n')[1:]
        lines = [i.split(';') for i in lines]
        res = []

        for i in lines:
            try:
                student_id = int(i[0])
                group_id = int(i[1])
                object_id = int(i[2])
                res.append((None, StudentInGroup(student_id, group_id, object_id)))
            except IndexError as e:
                exception_text = f"Строка {lines.index(i) + 1} не добавилась в [res]"
                print(exception_text)
                print(e)
                res.append((exception_text, None))
            except Exception as e:
                exception_text = f"Неизвестная ошибка в Student_in_group.parse():\n{e}"
                print(exception_text)
                res.append((exception_text, None))

        return res

    def __str__(self):
        return f''

    def __dict__(self) -> dict:
        return {'student_id': self.__student_id,
                'group_id': self.__group_id,
                'object_id': self._object_id}

