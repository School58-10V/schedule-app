import json
from datetime import datetime
from typing import List


class FileSource:
    # Метод  __init__ принимает путь до файла, с которым будут работать остальные методы и сохраняет его в private
    # переменную(по умолчанию "./db").
    def __init__(self, dp_path: str = '../db'):
        self.__dp_path = dp_path
        self.dictionary = {"group": 101,
                           "lesson": 102,
                           "lesson_row": 103,
                           "location": 104,
                           "no_learning_period": 105,
                           "student": 106,
                           "student_in_group": 107,
                           "subject_lesson": 108,
                           "teacher": 109,
                           "teachers_on_lesson_rows": 110,
                           "timetable": 111}

    def get_by_query(self, collection_name: str, query: dict):
        dict_list = self.__read_json_db(collection_name)
        # это коллекция словарей
        list_of_dicts = []
        for i in dict_list:
            # тут мы берём по 1 словарю из коллекции
            matching_keys = 0
            # это счётчик совпадений в словарях
            for j in query:
                if j in i and i[j] == query[j]:
                    matching_keys += 1
                    # если один ключ в query и словаре равен одному значению + 1 к совпадению
            if matching_keys == len(query):
                list_of_dicts.append(i)
                # если кол-во совпадений = кол-во ключей в query то словарь подходит
        return list_of_dicts
        # возвращаем список из подходяших словарей

    # Метод get_all принимает имя коллекции и возвращает все объекты коллекции в представлении Python(напр. все объекты
    # класса Location можно получить, если использовать get_all("Location"))
    def get_all(self, collection_name: str) -> List[dict]:
        # Возвращаем сформированный список, прочитанный методом __read_json_db.
        return self.__read_json_db(collection_name)

    # Метод get_by_id принимает имя коллекции и ID конкретного экземпляра класса, после чего возвращает dict всех
    # переменных данного экземпляра класса.
    def get_by_id(self, collection_name: str, object_id: int) -> dict:
        # Перебираем все объекты коллекции и сравниваем их с необходимым ID экземпляра класса. При совпадении
        # возвращаем dict всех переменных данного экземпляра класса. При отсутствии совпадений возвращает None
        for cnt in self.__read_json_db(collection_name):
            if cnt['object_id'] == object_id:
                return cnt
        return {None: None}

    # Предложения по назначению ID-шников(Оля). После номеров класса стоит добавлять время в микросекудах. Таким
    # образом мы получим айдишник, который можно будет понимать и без словаря обозначений. Например экземпляр класса
    # location может быть записан по ID, как 104412494(где 04- код класса, а 412494- микросекунды в момент записи ID).
    # уникальным(Ваня).
    # group - 101
    # lesson - 102
    # lesson_row - 103
    # location - 104
    # no_learning_period - 105
    # student - 106
    # student_in_group - 107
    # subject_lesson - 108
    # teacher - 109
    # teachers_on_lesson_rows - 110
    # timetable - 111

    # принимает на вход имя коллекции и dict объект для сохранения
    # добавляем словарь в список
    # записываем обратно в фаил
    def insert(self, collection_name: str, document: dict) -> dict:
        current_records = self.__read_json_db(collection_name)
        document["object_id"] = int(str(self.dictionary[collection_name]) + str(FileSource.generate_id()))
        current_records.append(document)
        target_json = self.__class__.serialize_records_to_json(current_records)
        with open(f"{self.__dp_path}/{collection_name}.json", mode="w", encoding='utf-8') as data_file:
            data_file.write(target_json)
        return document

    # Метод update принимает на вход имя коллекции и dict объект для изменения имеюшегося и его айди.
    # Мы ишим подходяший обьект, добавляем изменённые данные, чистим список
    # добавляем изменёный и записываем обратно в фаил
    def update(self, collection_name: str, object_id: int, document: dict) -> dict:
        current_records = self.__read_json_db(collection_name)
        current_records_copy = self.__read_json_db(collection_name)
        founded_id = False
        for i in current_records:
            if i["object_id"] == object_id:
                # проверяем, есть ли обжект айди в документе
                founded_id = True
                new_dict = i
                new_dict.update(document)
                current_records_copy.remove(i)
                current_records_copy.append(new_dict)
        target_json = self.__class__.serialize_records_to_json(current_records_copy)
        with open(f"{self.__dp_path}/{collection_name}.json", mode="w", encoding='utf-8') as data_file:
            data_file.write(target_json)
        if founded_id is True:
            return new_dict
        return {None: None}

    # Метод delete принимает на вход имя коллекции и айди обьекта которого надо удалить.
    # Мы ишим подходяший обьект, удаляем его
    # добавляем изменёный список и записываем обратно в фаил
    def delete(self, collection_name: str, object_id: int) -> dict:
        current_records = self.__read_json_db(collection_name)
        del_dct = {}
        for dct in current_records:
            if dct["object_id"] == object_id:
                current_records.remove(dct)
                del_dct = dct
                break
        target_json = self.__class__.serialize_records_to_json(current_records)
        with open(f"{self.__dp_path}/{collection_name}.json", mode="w", encoding='utf-8') as data_file:
            data_file.write(target_json)
        return del_dct.pop("object_id")  # new удаленный объект без обжект айди

    # __read_json_db подвергся некоторым изменениям, в частности на ввод был добавлен аргумент collection_name- он
    # принимает имя файла, чтобы данную функцию стало возможно применять для любого класса
    def __read_json_db(self, collection_name: str) -> List[dict]:
        try:
            with open(f"{self.__dp_path}/{collection_name}.json",
                      mode="r", encoding='utf-8') as data_file:
                record = json.loads(data_file.read())
                return record
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return []

    @staticmethod
    def serialize_records_to_json(records: list, indent: int = None) -> str:
        return json.dumps(records, ensure_ascii=False, indent=indent)

    @staticmethod
    def generate_id():
        return datetime.microsecond
