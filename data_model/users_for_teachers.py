from __future__ import annotations  # нужно чтобы parse мог быть типизирован

from typing import Optional, List, TYPE_CHECKING

from adapters.abstract_source import AbstractSource
from data_model.abstract_model import AbstractModel

if TYPE_CHECKING:
    from adapters.db_source import DBSource
    from data_model.user import User
    from data_model.teacher import Teacher


class UsersForTeachers(AbstractModel):
    """
        user_id - айди пользователя
        teacher_id - айди учителя
        object_id - айди связи
    """

    def __init__(self, db_source: DBSource, user_id: int, teacher_id: int, object_id: Optional[int] = None):
        super().__init__(db_source)
        self.__user_id = user_id
        self.__teacher_id = teacher_id
        self._object_id = object_id

    @classmethod
    def _get_collection_name(cls) -> str:
        return cls.__name__

    def get_user_id(self) -> int:
        return self.__user_id

    def get_teacher_id(self) -> int:
        return self.__teacher_id

    def __str__(self) -> str:
        return f''

    def __dict__(self) -> dict:
        return {'user_id': self.get_user_id(),
                'teacher_id': self.get_teacher_id(),
                'object_id': self.get_main_id()}

    @classmethod
    def get_user_by_teacher_id(cls, teacher_id: int, db_source: AbstractSource) -> List[User]:
        from data_model.user import User
        return [User.get_by_id(i['user_id'], db_source=db_source)
                for i in db_source.get_by_query(cls._get_collection_name(), {'teacher_id': teacher_id})]

    @classmethod
    def get_teacher_by_user_id(cls, user_id: int, db_source: AbstractSource) -> List[Teacher]:
        from data_model.teacher import Teacher
        return [Teacher.get_by_id(i['teacher_id'], db_source=db_source)
                for i in db_source.get_by_query(cls._get_collection_name(), {'user_id': user_id})]

    @classmethod
    def get_by_user_and_teacher_id(cls, user_id: int, teacher_id: int,
                                    db_source: AbstractSource) -> List[UsersForTeachers]:
        res = []
        for i in db_source.get_by_query(cls._get_collection_name(), {"teacher_id": teacher_id, 'user_id': user_id}):
            res.append(cls(**i, db_source=db_source))
        return res
