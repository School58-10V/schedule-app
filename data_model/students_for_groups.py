from __future__ import annotations  # нужно чтобы parse мог быть типизирован

from typing import Optional, List, TYPE_CHECKING

from adapters.abstract_source import AbstractSource
from data_model.abstract_model import AbstractModel

if TYPE_CHECKING:
    from adapters.db_source import DBSource
    from data_model.group import Group
    from data_model.student import Student


class StudentsForGroups(AbstractModel):
    """
        Класс ученика в группе. Используется для m2m отношения между
        Group и Student
        student_id - айди ученика
        group_id - айди группы
        object_id - айди группы учeников
    """

    def __init__(self, db_source: DBSource, student_id: int,
                 group_id: int, object_id: Optional[int] = None):
        super().__init__(db_source)
        self.__student_id = student_id
        self.__group_id = group_id
        self._object_id = object_id

    @classmethod
    def _get_collection_name(cls) -> str:
        return cls.__name__

    def get_student_id(self) -> int:
        return self.__student_id

    def get_group_id(self) -> int:
        return self.__group_id

    def __str__(self) -> str:
        return f''

    def __dict__(self) -> dict:
        return {'student_id': self.get_student_id(),
                'group_id': self.get_group_id(),
                'object_id': self.get_main_id()}

    @classmethod
    def get_group_by_student_id(cls, student_id: int, db_source: AbstractSource) -> List[Group]:
        from data_model.group import Group
        return [Group.get_by_id(i['group_id'], db_source=db_source)
                for i in db_source.get_by_query(cls._get_collection_name(), {'student_id': student_id})]

    @classmethod
    def get_groups_ids_for_student(cls, student_id: int, db_source: AbstractSource) -> List[int]:
        return [i['group_id'] for i in db_source.get_by_query(cls._get_collection_name(), {'student_id': student_id})]

    @classmethod
    def get_student_by_group_id(cls, group_id: int, db_source: AbstractSource) -> List[Student]:
        from data_model.student import Student
        return [Student.get_by_id(i['student_id'], db_source=db_source)
                for i in db_source.get_by_query(cls._get_collection_name(), {'group_id': group_id})]

    @classmethod
    def get_by_student_and_group_id(cls, group_id: int, student_id: int,
                                    db_source: AbstractSource) -> List[StudentsForGroups]:
        res = []
        # Проходим циклом по списку словарей с данными про объекты,
        # в которых student_id и group_id, которые нам нужны
        # и переводим их в объекты класса
        for i in db_source.get_by_query(cls._get_collection_name(), {"student_id": student_id, 'group_id': group_id}):
            res.append(cls(**i, db_source=db_source))
        return res
