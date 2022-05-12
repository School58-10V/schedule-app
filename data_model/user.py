from __future__ import annotations  # нужно чтобы parse мог быть типизирован

from data_model.abstract_model import AbstractModel
from typing import List, Optional, TYPE_CHECKING
from data_model.parsed_data import ParsedData
import hashlib

if TYPE_CHECKING:
    from adapters.db_source import DBSource


class User(AbstractModel):

    def __init__(self, db_source: DBSource, name: str, login: str, hash_password: Optional[str] = None,
                 password: Optional[str] = None, object_id: int = None):
        super().__init__(db_source)
        self.__login = login
        if hash_password is None and password is not None:
            self.__password_hash = hashlib.sha256(password.encode()).hexdigest()
        elif password is None and hash_password is not None:
            self.__password_hash = hash_password
        else:
            raise ValueError('Ошибка создания: должен присутствовать password ИЛИ hash_password')
        self.__name = name
        self.__object_id = object_id
        """
            :param db_source: ссылка на бд
            :param login: логин
            :param password_hash: пароль
            :param name: имя пользователя
        """

    @classmethod
    def get_by_login(cls, login: str, db_source: DBSource) -> Optional[User]:
        data = db_source.get_by_query(collection_name=cls._get_collection_name(), query={'login': login})
        if len(data) == 0:
            raise ValueError('No data was given')
        if len(data) > 1:
            raise ValueError('Too many results')
        return User(**data[0], db_source=db_source)

    def get_login(self) -> str:
        return self.__login

    def get_password_hash(self) -> str:
        return self.__password_hash

    def get_name(self) -> str:
        return self.__name

    def get_main_id(self) -> int:
        return self.__object_id

    def __str__(self):
        return f"Пользователь {self.get_name()} с логином {self.get_login()}"

    def __dict__(self) -> dict:
        return {"name": self.get_name(),
                "login": self.get_login(),
                "hash_password": self.get_password_hash(),
                'object_id': self.get_main_id()}

    def compare_hash(self, password: str) -> bool:
        return self.__password_hash == hashlib.sha256(password.encode()).hexdigest()
