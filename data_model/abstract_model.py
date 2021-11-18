from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import Optional, List


class AbstractModel(ABC):
    """
        Абстрактный класс модели,
    """

    def save(self, output_path: str = './db'):
        current_records = self._read_json_db(output_path)
        current_records.append(self.__dict__())
        target_json = self.__class__._serialize_records_to_json(current_records)
        with open(f"{output_path}/{type(self).__name__}.json", mode="w", encoding='utf-8') as data_file:
            data_file.write(target_json)
        return self

    def delete(self, db_path: str = './db'):
        if self._object_id is None:
            return self
        data = self._read_json_db(db_path)
        for i, j in enumerate(data):
            if j['object_id'] == self._object_id:
                del data[i]
                new_data = self._serialize_records_to_json(data)
                with open(f"{db_path}/{type(self).__name__}.json", mode="w", encoding='utf-8') as data_file:
                    data_file.write(new_data)
                break
        self._set_main_id(None)
        return self

    def serialize_to_json(self, indent: Optional[int] = None) -> str:
        return json.dumps(self.__dict__(), ensure_ascii=False, indent=indent)

    @classmethod
    def get_all(cls, db_path: str = "./db") -> List[AbstractModel]:
        # нужно убедиться чтобы **i работало, т.е. __dict__ и __init__ имели одинаковые названия аргументов
        return [cls(**i) for i in cls._read_json_db(db_path)]

    @classmethod
    def get_by_id(cls, element_id: int, db_path: str = "./db") -> AbstractModel:
        for i in cls._read_json_db(db_path):
            if i['object_id'] == element_id:
                return cls(**i)
        raise ValueError(f"Объект с id {element_id} не найден")

    @classmethod
    def _read_json_db(cls, db_path: str) -> List[dict]:
        try:
            with open(f"{db_path}/{cls.__name__}.json",
                      mode="r", encoding='utf-8') as data_file:
                record = json.loads(data_file.read())
                return record
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return []

    @staticmethod
    def _serialize_records_to_json(records: List[dict], indent: Optional[int] = None) -> str:
        return json.dumps(records, ensure_ascii=False, indent=indent)

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __dict__(self):
        pass

    def get_main_id(self):
        return self._object_id

    def _set_main_id(self, elem_id: Optional[int] = None):
        self._object_id = elem_id
        return self
