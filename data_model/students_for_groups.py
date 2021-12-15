from __future__ import annotations  # нужно чтобы parse мог быть типизирован

from data_model.parsed_data import ParsedData
from typing import Optional, List, TYPE_CHECKING

from data_model.abstract_model import AbstractModel

if TYPE_CHECKING:
    from adapters.file_source import FileSource
    from data_model.group import Group


class StudentsForGroups(AbstractModel):
    """
        Класс ученика в группе. Используется для m2m отношения между
        Group и Student
        student_id - айди ученика
        group_id - айди группы
        object_id - айди группы учeников
    """

    def __init__(self, db_source: FileSource, student_id: int,
                 group_id: int, object_id: Optional[int] = None):
        super().__init__(db_source)
        self.__student_id = student_id
        self.__group_id = group_id
        self._object_id = object_id

    def get_student_id(self) -> int:
        return self.get_student_id()

    def get_group_id(self) -> int:
        return self.__group_id

    @staticmethod
    def parse(file_location: str, db_source: FileSource) -> List[(Optional[str], Optional[StudentsForGroups])]:
        f = open(file_location, encoding='utf-8')
        lines = f.read().split('\n')[1:]
        lines = [i.split(';') for i in lines]
        res = []

        for i in lines:
            try:
                student_id = int(i[0])
                group_id = int(i[1])
                res.append(ParsedData(None, StudentsForGroups(student_id=student_id,
                                                              group_id=group_id, db_source=db_source)))
            except IndexError as e:
                exception_text = f"Строка {lines.index(i) + 1} не добавилась в [res]"
                print(exception_text)
                print(e)
                res.append(ParsedData(exception_text, None))
            except Exception as e:
                exception_text = f"Неизвестная ошибка в Student_in_group.parse():\n{e}"
                print(exception_text)
                res.append(ParsedData(exception_text, None))

        return res

    def __str__(self):
        return f''

    def __dict__(self) -> dict:
        return {'student_id': self.get_student_id(),
                'group_id': self.get_group_id(),
                'object_id': self.get_main_id()}

    @classmethod
    def get_group_by_student_id(cls, student_id: int, db_source: FileSource) -> List[Group]:
        from data_model.group import Group
        return [Group.get_by_id(i['group_id'], db_source=db_source)
                for i in db_source.get_by_query(cls._get_collection_name(), {'student_id': student_id})]
