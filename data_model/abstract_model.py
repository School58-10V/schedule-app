from __future__ import annotations
import json
from abc import ABC, abstractmethod
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from adapters.db_source import DBSource


class AbstractModel(ABC):
    """
        Абстрактный класс сущности
    """

    def __init__(self, db_source: DBSource):
        self._db_source = db_source

    @classmethod
    def _get_collection_name(cls) -> str:
        # if cls.__name__[-1] == 's':
        #     return cls.__name__
        return cls.__name__ + 's'

    def save(self) -> AbstractModel:
        if self.get_main_id() is None:
            result = self._db_source.insert(self._get_collection_name(), self.__dict__())
            self._set_main_id(result['object_id'])
        else:
            self._db_source.update(self._get_collection_name(), self.get_main_id(), self.__dict__())
        return self

    def delete(self) -> AbstractModel:
        if self.get_main_id() is not None:
            self._db_source.delete(self._get_collection_name(), self.get_main_id())
            self._set_main_id(None)
        return self

    def serialize_to_json(self, indent: Optional[int] = None) -> json:
        """
        Превращает данный объект класса в JSON-строку

        :param indent: табуляция для полученной строки json-а
        :return: json-строку
        """
        return json.dumps(self.__dict__(), ensure_ascii=False, indent=indent)

    @classmethod
    def get_all(cls, db_source: DBSource) -> List[AbstractModel]:
        """
        Возвращает все данные из сохранений в формате объектов соответствующих классов

        :param db_source: data_source объект
        :return: Список всех объектов этого класса
        """
        return [cls(**obj, db_source=db_source) for obj in db_source.get_all(cls._get_collection_name())]

    @classmethod
    def get_by_id(cls, element_id: int, db_source: DBSource) -> AbstractModel:
        """
        Возвращает запрошенный по element_id объект класса по данным из сохранений

        :param element_id: айдишник объекта
        :param db_source: data_source объект
        :return: Объект этого класса с таким идшником
        """

        obj = db_source.get_by_id(cls._get_collection_name(), element_id)
        return cls(**obj, db_source=db_source)

    @classmethod
    def get_by_query(cls, query: dict, db_source: DBSource) -> List[AbstractModel]:
        """
        Возвращает запрошенный по query объект класса по данным из сохранений

        :param query: пары ключ-значение для поиска
        :param db_source: data_source объект
        :return: Объект этого класса с таким идшником
        """

        obj = db_source.get_by_query(cls._get_collection_name(), query)
        return [cls(**el, db_source=db_source) for el in obj]

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __dict__(self):
        pass

    def get_db_source(self) -> DBSource:
        return self._db_source

    def get_main_id(self) -> int:
        """
        Возвращает айди текущего объекта

        :return: айдишнк текущего объекта
        """
        return self._object_id

    def _set_main_id(self, elem_id: Optional[int] = None) -> AbstractModel:
        """
        Меняет айди текущего объекта на предоставленное значение

        :param elem_id: новый айдишник
        :return: текущий объект
        """
        self._object_id = elem_id
        return self
