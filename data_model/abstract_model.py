from __future__ import annotations
import json
from abc import ABC, abstractmethod
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from adapters.abstract_source import AbstractSource


class AbstractModel(ABC):
    """
        Абстрактный класс сущности
    """

    def __init__(self, source: AbstractSource):
        self._source = source

    @classmethod
    def _get_collection_name(cls) -> str:
        # if cls.__name__[-1] == 's':
        #     return cls.__name__
        return cls.__name__ + 's'

    def save(self) -> AbstractModel:
        if self.get_main_id() is None:
            result = self._source.insert(self._get_collection_name(), self.__dict__())
            self._set_main_id(result['object_id'])
        else:
            self._source.update(self._get_collection_name(), self.get_main_id(), self.__dict__())
        return self

    def delete(self) -> AbstractModel:
        if self.get_main_id() is not None:
            self._source.delete(self._get_collection_name(), self.get_main_id())
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
    def get_all(cls, source: AbstractSource) -> List[AbstractModel]:
        """
        Возвращает все данные из сохранений в формате объектов соответствующих классов

        :param source: объект источника данных
        :return: Список всех объектов этого класса
        """
        return [cls(**obj, source=source) for obj in source.get_all(cls._get_collection_name())]

    @classmethod
    def get_by_id(cls, element_id: int, source: AbstractSource) -> AbstractModel:
        """
        Возвращает запрошенный по element_id объект класса по данным из сохранений

        :param element_id: айдишник объекта
        :param source: data_source объект
        :return: Объект этого класса с таким идшником
        """

        obj = source.get_by_id(cls._get_collection_name(), element_id)
        return cls(**obj, source=source)

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __dict__(self):
        pass

    def get_source(self) -> AbstractSource:
        """
        Возвращает источник с которым мы работаем
        """
        return self._source

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
