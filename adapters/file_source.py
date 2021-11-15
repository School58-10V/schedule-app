import json
from datetime import datetime


class FileSource:
    # Метод  __init__ принимает путь до файла, с которым будут работать остальные методы и сохраняет его в private
    # переменную(по умолчанию "./db").
    def __init__(self, dp_path: str = './db'):
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

    def generate_id(self):
        return datetime.microsecond

    def __dp_path(self):
        return self.__dp_path

    # Метод get_all принимает имя коллекции и возвращает все объекты коллекции в представлении Python(напр. все объеты
    # класса Location можно получить, если использовать get_all("Location"))
    @classmethod
    def get_all(cls, collection_name: str) -> list[dict]:
        # Возвращаем сформированный список, прочитанный методом __read_json_db.
        return cls.__read_json_db(cls.__dp_path(), collection_name)

    # Метод get_by_id принимает имя коллекции и ID конкретного экземпляра класса, после чего возвращает dict всех
    # переменных данного экземпляра класса.
    @classmethod
    def get_by_id(cls, collection_name: str, element_id: int) -> dict:
        # Перебираем все объекты коллекции и сравниваем их с необходимым ID экземпляра класса. При совпадении
        # возвращаем dict всех переменных данного экземпляра класса. При отсутствии совпадений возвращает None
        for i in cls.__read_json_db(cls.__dp_path(), collection_name):
            if i['group_id'] == element_id:
                return i
        return None

    def get_by_query(self, collection_name: str, query: dict[str, Any]) -> list[dict]:
        pass

    # Предложения по назначению ID-шников(Оля). После номеров класса стоит добавлять порядковый номер экземпляра. Таким
    # образом мы получим айдишник, который можно будет понимать и без словаря обозначений. Например 4 экземпляр класса
    # location будет записан по ID, как 044, а 18 экземпляр класса teacher, как 0918, так каждый ID будет
    # уникальным(Ваня).
    # group - 01
    # lesson - 02
    # lesson_row - 03
    # location - 04
    # no_learning_period - 05
    # student - 06
    # student_in_group - 07
    # subject_lesson - 08
    # teacher - 09
    # teachers_on_lesson_rows - 10
    # timetable - 11
    # принимает на вход имя коллекции и dict объект для сохранения. Метод Insert сохраняет новый(!) объект и ничего не
    # возвращает. id_class - первая часть ID, которая отвечает за определитель класса. Не определена, так как не приняты
    # нормативы составления ID.
    def insert(self, collection_name: str, document: dict) -> dict:
        with open(f"./db/{collection_name}.json", mode="w", encoding='utf-8') as data_file:
            current_records = self.__read_json_db(collection_name)
            document["_object_id"] = int(str(self.dictionary[collection_name]) + str(FileSource.generate_id()))
            current_records.append(document)
            target_json = self.__class__.serialize_records_to_json(current_records)
            data_file.write(target_json)
        return {None: None}  # заглушка, потом решим, что с этим делать

    def update(self, collection_name: str, _object_id: int, document: dict) -> dict:
        pass

    def delete(self, collection_name: str, _object_id: int) -> dict:
        with open(f"./db/{collection_name}.json", mode="w", encoding='utf-8') as data_file:
            current_records = self.__read_json_db(collection_name)

            target_json = self.__class__.serialize_records_to_json(current_records)
            data_file.write(target_json)

    # __read_json_db подвергся некоторым изменениям, в частности на ввод был добавлен аргумент collection_name- он
    # принимает имя файла, чтобы данную функцию стало возможно применять для любого класса
    @classmethod
    def __read_json_db(cls, db_path, collection_name) -> list:
        try:
            with open(f"{db_path}/{collection_name}.json",
                      mode="r", encoding='utf-8') as data_file:
                record = json.loads(data_file.read())
                return record
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return []

    @staticmethod
    def serialize_records_to_json(records: list, indent: int = None) -> str:
        return json.dumps(records, ensure_ascii=False, indent=indent)
