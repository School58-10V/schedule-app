from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import Optional, List


class AbstractModel(ABC):
    """
        Абстрактный класс модели
    """

    # Добавляет данные текущего объекта в конец сохранения используя __dict__() этого класса
    def save(self, output_path: str = './db'):
        current_records = self._read_json_db(output_path)  # Читает старую версию файла и записывает список словарей
        current_records.append(self.__dict__())  # Добавляет настоящий объект
        target_json = AbstractModel._serialize_records_to_json(current_records)  # Готовит данные для формата JSON
        with open(f"{output_path}/{type(self).__name__}.json", mode="w", encoding='utf-8') as data_file:
            data_file.write(target_json)
        return self  # Возвращает объект который был сохранён

    # Удаляет сохранения и id-связи текущего объекта
    def delete(self, db_path: str = './db'):
        if self._object_id is None:  # Проверяет валидность данного объекта
            return self
        data = self._read_json_db(db_path)  # Читает файл сохранения и возвращает список словарей
        for i, j in enumerate(data):  # Бежит по data и записывает в i индекс словаря, а в j сам словарь
            if j['object_id'] == self._object_id:  # Проверяет совпадение искомого айдишника с словарём в j
                del data[i]
                # Делает новую версию данных без удалённого словаря
                new_data = AbstractModel._serialize_records_to_json(data)
                with open(f"{db_path}/{type(self).__name__}.json", mode="w", encoding='utf-8') as data_file:
                    data_file.write(new_data)  # Перезаписывает сохранение новыеми данными
                break
        self._set_main_id(None)  # В любом случае уничтожает все id-связи данного объекта
        return self  # Возвращает удалённый объект с self._object_id = None

    # Превращает один обьект в JSON-строку
    def serialize_to_json(self, indent: Optional[int] = None) -> str:
        return json.dumps(self.__dict__(), ensure_ascii=False, indent=indent)

    @classmethod
    # Возвращает все данные из сохранений в формате объектов соответствующих классов
    def get_all(cls, db_path: str = "./db") -> List[AbstractModel]:
        return [cls(**i) for i in cls._read_json_db(db_path)]

    @classmethod
    # Возвращает запрощенный по element_id объект класса по данным из сохранений
    def get_by_id(cls, element_id: int, db_path: str = "./db") -> AbstractModel:
        for i in cls._read_json_db(db_path):  # Проходит по списку словарей в файле сохранения
            if i['object_id'] == element_id:
                return cls(**i)
        raise ValueError(f"Объект с id {element_id} не найден")

    @classmethod
    # Читает файл сохранения текущего объекта и возращает пустой список при ошибке
    def _read_json_db(cls, db_path: str) -> List[dict]:
        try:
            with open(f"{db_path}/{cls.__name__}.json",
                      mode="r", encoding='utf-8') as data_file:
                record = json.loads(data_file.read())
                return record
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return []

    @staticmethod
    # Подготавливает входные данные к записи в JSON и возвращает JSON-строку
    def _serialize_records_to_json(records: List[dict], indent: Optional[int] = None) -> str:
        return json.dumps(records, ensure_ascii=False, indent=indent)

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __dict__(self):
        pass

    # Возвращает айди текущего объекта
    def get_main_id(self):
        return self._object_id

    # Меняет айди текущего объекта на предоставленное значение
    def _set_main_id(self, elem_id: Optional[int] = None):
        self._object_id = elem_id
        return self
