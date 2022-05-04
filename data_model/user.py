from __future__ import annotations  # нужно чтобы parse мог быть типизирован

from data_model.abstract_model import AbstractModel
from typing import List, Optional, TYPE_CHECKING
from data_model.parsed_data import ParsedData
import hashlib

if TYPE_CHECKING:
    from adapters.db_source import DBSource


class User(AbstractModel):

    def __init__(self, name: str, login: str, hash_password: str, db_source: DBSource):
        super().__init__(db_source)
        self.__login = login
        self.__password_hash = hash_password
        self.__name = name
        """
            :param db_source: ссылка на бд
            :param login: логин
            :param password_hash: пароль
            :param name: имя пользователя
        """

    @classmethod
    def get_by_login(cls, login: str, db_source: DBSource) -> Optional[User]:
        data = db_source.get_by_query(collection_name=cls._get_collection_name(), query={'login': login})
        # Надо написать метод в адапторе, чтобы лазить в базу и там эти ошибки выдавать. Пока здесь
        if len(data) == 0:
            return None
        return User(**data[0], db_source=db_source)

    def get_login(self) -> str:
        return self.__login

    def get_password_hash(self) -> str:
        return self.__password_hash

    def get_name(self) -> str:
        return self.__name

    def get_main_id(self):
        return self.get_login()

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

    def save(self):
        if not self.get_by_login(login=self.get_login(), db_source=self.get_db_source()):
            result = self._db_source.insert(self._get_collection_name(), self.__dict__())
        else:
            self._db_source.update(self._get_collection_name(), f"'{self.get_main_id()}'",
                                   self.__dict__(), foreign_key='login')
        return self

    def delete(self):
        if self.get_main_id() is not None:
            self._db_source.delete(self._get_collection_name(), f"'{self.get_main_id()}'", foreign_key='login')
            self.__login = None
        return self
