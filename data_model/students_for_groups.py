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

    #    @staticmethod
    #    def parse(file_location: str, db_source: DBSource) -> List[(Optional[str], Optional[StudentsForGroups])]:
    #        f = open(file_location, encoding='utf-8')
    #        lines = f.read().split('\n')[1:]
    #        lines = [i.split(';') for i in lines]
    #        res = []
    #
    #        for i in lines:
    #            try:
    #                student_id = int(i[0])
    #                group_id = int(i[1])
    #                res.append(ParsedData(None, StudentsForGroups(student_id=student_id,
    #                                                             group_id=group_id, db_source=db_source)))
    #            except IndexError as e:
    #                exception_text = f"Строка {lines.index(i) + 1} не добавилась в [res]"
    #                print(exception_text)
    #                print(e)
    #                res.append(ParsedData(exception_text, None))
    #            except Exception as e:
    #                exception_text = f"Неизвестная ошибка в Student_in_group.parse():\n{e}"
    #                print(exception_text)
    #                res.append(ParsedData(exception_text, None))
    #
    #        return res

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
