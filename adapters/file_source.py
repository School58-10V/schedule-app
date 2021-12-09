import json
import datetime
from typing import List


class FileSource:
    # Метод  __init__ принимает путь до файла, с которым будут работать остальные методы и сохраняет его в private
    # переменную(по умолчанию "./db").
    def __init__(self, dp_path: str = './db'):
        self.__dp_path = dp_path
        self.dictionary = {"Group": 101,
                           "Lesson": 102,
                           "LessonRow": 103,
                           "Location": 104,
                           "NoLearningPeriod": 105,
                           "Student": 106,
                           "StudentInGroup": 107,
                           "Subject": 108,
                           "Teacher": 109,
                           "TeachersOnLessonRows": 110,
                           "TimeTable": 111}

    def get_by_query(self, collection_name: str, query: dict):
        dict_list = self.__read_json_db(collection_name)
        # это коллекция словарей
        list_of_dicts = []
        for dct in dict_list:
            # тут мы берём по 1 словарю из коллекции
            matching_keys = 0
            # это счётчик совпадений в словарях
            for j in query:
                if j in dct and dct[j] == query[j]:
                    matching_keys += 1
                    # если один ключ в query и словаре равен одному значению + 1 к совпадению
            if matching_keys == len(query):
                list_of_dicts.append(dct)
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
        raise ValueError(f'Объект с id {object_id} из {collection_name} не существует')

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

    def check_unique_id(self, collection_name: str, object_id: int) -> bool:
        # проверяет уникальность айди у объекта
        current_records = self.__read_json_db(collection_name)
        for i in current_records:
            if i["object_id"] == object_id:
                return True
        return False

    def insert(self, collection_name: str, document: dict) -> dict:
        current_records = self.__read_json_db(collection_name)
        object_id = int(str(self.dictionary[collection_name]) + str(FileSource.generate_id()))
        # назначаем айди отдельно
        founded_id = self.check_unique_id(collection_name, object_id)
        if founded_id:  # уточнить эту строчку
            while founded_id:
                # проверяем его на уникальность
                object_id = int(str(self.dictionary[collection_name]) + str(FileSource.generate_id()))
                # назначаем айди каждый раз когда мы его проверяем
                founded_id = self.check_unique_id(collection_name, object_id)
                # каждую итерацию цикла проверяте существование id
        document["object_id"] = object_id  # вываливаясть из цикла, добавляет в документ строку с описанием id,
        # предавая значение id
        current_records.append(document)  # добавляем в список словарей отредактированный document
        target_json = self.__class__.serialize_records_to_json(current_records)  # переделывает
        # current_records в формат json
        with open(f"{self.__dp_path}/{collection_name}.json", mode="w", encoding='utf-8') as data_file:
            data_file.write(target_json)
        return document  # возвращаем отредактированный документ

    # Метод update принимает на вход колекцию словарей, id объекта, который ты хочешь изменить и изменения,
    # которые мы хотим внести в этот объект.
    def update(self, collection_name: str, object_id: int, document: dict) -> dict:
        founded_id = self.check_unique_id(collection_name, object_id)
        if not founded_id:
            return {None: None}
        current_records = self.__read_json_db(collection_name)
        new_dict = {None, None}  # глобальная прееменная для цикла
        if "object_id" in document:
            del document["object_id"]  # удаляем из изменений id, чтобы он не перезаписался.
        for dct in current_records:
            if dct["object_id"] == object_id:
                new_dict = dct  # чтобы не портить dct, тк потом будем искать эту переменную в current_records
                new_dict.update(document)
                del current_records[current_records.index(dct)]  # перезаписываем измененный dict
                current_records.append(new_dict)
                break
        target_json = self.__class__.serialize_records_to_json(current_records)
        with open(f"{self.__dp_path}/{collection_name}.json", mode="w", encoding='utf-8') as data_file:
            data_file.write(target_json)
        return new_dict

    # Метод delete принимает на вход имя коллекции и id обьекта, который надо удалить.
    def delete(self, collection_name: str, object_id: int) -> dict:
        current_records = self.__read_json_db(collection_name)
        del_dct = {}
        founded_id = self.check_unique_id(collection_name, object_id)
        if founded_id:
            for dct in current_records:
                if dct["object_id"] == object_id:  # совпадют ли воводимый id c id текущего объекта в итерации
                    del current_records[current_records.index(dct)]
                    del_dct = dct
                    break
            target_json = self.__class__.serialize_records_to_json(current_records)
            del del_dct["object_id"]
            with open(f"{self.__dp_path}/{collection_name}.json", mode="w", encoding='utf-8') as data_file:
                data_file.write(target_json)
                return del_dct
        return {None: None}

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
        return round(datetime.datetime.utcnow().timestamp() * 1000)
