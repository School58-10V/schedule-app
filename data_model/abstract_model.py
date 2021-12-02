from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import Optional, List


class AbstractModel(ABC):
    """
        Абстрактный класс сущности
    """

    def serialize_to_json(self, indent: Optional[int] = None) -> str:
        """
        Превращает данный объект класса в JSON-строку

        :param indent: табуляция для полученной строки json-а
        :return: json-строку
        """
        return json.dumps(self.__dict__(), ensure_ascii=False, indent=indent)

    @classmethod
    def get_all(cls, db_path: str = "./db") -> List[AbstractModel]:
        """
        Возвращает все данные из сохранений в формате объектов соответствующих классов

        :param db_path: путь до папки с .json файлами
        :return: Список всех объектов этого класса
        """
        return [cls(**i) for i in cls._read_json_db(db_path)]

    @classmethod
    def get_by_id(cls, element_id: int, db_path: str = "./db") -> AbstractModel:
        """
        Возвращает запрощенный по element_id объект класса по данным из сохранений

        :param element_id: айдишник объекта
        :param db_path: путь до папки с .json файлами
        :return: Объект этого класса с таким идшником
        """
        # Проходит по списку словарей в файле сохранения
        for i in cls._read_json_db(db_path):
            if i['object_id'] == element_id:
                return cls(**i)
        raise ValueError(f"Объект с id {element_id} не найден")

    @classmethod
    def _read_json_db(cls, db_path: str) -> List[dict]:
        """
        Читает файл сохранения текущего объекта и возращает пустой список при ошибке

        :param db_path: путь до папки с .json файлами
        :return:
        """
        try:
            with open(f"{db_path}/{cls.__name__}.json",
                      mode="r", encoding='utf-8') as data_file:
                record = json.loads(data_file.read())
                return record
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return []

    @staticmethod
    def _serialize_records_to_json(records: List[dict], indent: Optional[int] = None) -> str:
        """
        Подготавливает входные данные к записи в JSON

        :param records: список словарей каких-то объектов
        :param indent: табуляция для полученной строки json-а
        :return: json-строку
        """
        return json.dumps(records, ensure_ascii=False, indent=indent)

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __dict__(self):
        pass

    def get_main_id(self):
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
