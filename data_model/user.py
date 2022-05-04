from __future__ import annotations  # нужно чтобы parse мог быть типизирован

from data_model.abstract_model import AbstractModel
from typing import List, Optional, TYPE_CHECKING
from data_model.parsed_data import ParsedData
import hashlib

if TYPE_CHECKING:
    from adapters.db_source import DBSource


class User(AbstractModel):

    def __init__(self, name: str, login: str, password_hash: str, db_source: DBSource):
        super().__init__(db_source)
        self.__login = login
        self.__password_hash = password_hash
        self.__name = name
        """
            :param db_source: ссылка на бд
            :param login: логин
            :param password_hash: пароль
            :param name: имя пользователя
        """

    @classmethod
    def get_by_login(cls, login: str, db_source: DBSource) -> User:
        data = db_source.get_by_query(collection_name=cls._get_collection_name(), query={'login': login})
        # Надо написать метод в адапторе, чтобы лазить в базу и там эти ошибки выдавать. Пока здесь
        if len(data) == 0:
            raise ValueError()
        return User(**data[0], db_source=db_source)

    def get_login(self) -> str:
        return self.__login

    def get_password_hash(self) -> str:
        return self.__password_hash

    def get_name(self) -> str:
        return self.__name

    def __str__(self):
        return f"Пользователь {self.get_name()} с логином {self.get_login()}"

    def __dict__(self) -> dict:
        return {"name": self.get_name(),
                "login": self.get_login(),
                "hash_password": self.get_password_hash()}

    def password_to_hash(self):
        self.__password_hash = hashlib.sha256(self.get_password_hash().encode()).hexdigest()

    def compare_hash(self, password: str) -> bool:
        return self.__password_hash == hashlib.sha256(password.encode()).hexdigest()
