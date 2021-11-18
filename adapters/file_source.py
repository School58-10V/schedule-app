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

    @classmethod
    def get_by_query(cls, collection_name, query) -> list[dict]:
        dict_list = cls.__read_json_db(cls.__dp_path(), collection_name)
        # это коллекция словарей
        matching_keys = {}
        list_of_dicts = []
        for i in dict_list:
            for j in i:
                if j in query:
                    # перебираем ключи
                    # и если они совпадают добовляем
                    matching_keys.update(j)
            list_of_dicts.append(matching_keys)
            # собираем словари в список и реторним
        return list_of_dicts

    # Метод get_all принимает имя коллекции и возвращает все объекты коллекции в представлении Python(напр. все объеты
    # класса Location можно получить, если использовать get_all("Location"))
    def get_all(self, collection_name: str) -> list[dict]:
        # Возвращаем сформированный список, прочитанный методом __read_json_db.
        return cls.__read_json_db(cls.__dp_path(), collection_name)

    # Метод get_by_id принимает имя коллекции и ID конкретного экземпляра класса, после чего возвращает dict всех
    # переменных данного экземпляра класса.
    def get_by_id(cls, collection_name: str, object_id: int) -> dict:
        # Перебираем все объекты коллекции и сравниваем их с необходимым ID экземпляра класса. При совпадении
        # возвращаем dict всех переменных данного экземпляра класса. При отсутствии совпадений возвращает None
        for cnt in cls.__read_json_db(cls.__dp_path(), collection_name):
            if cnt['object_id'] == object_id:
                return cnt
        return None

    # Метод get_by_query на вход принимает имя коллекции и словарь
    @classmethod
    def get_by_query(cls, collection_name, query) -> list[dict]: # new везде надо указывать с чем лист
        dict_list = cls.__read_json_db(cls.__dp_path(), collection_name)
        # это коллекция словарей
        matching_keys = {}
        for cnt in dict_list:
            for cnt_2 in cnt:
                if cnt_2 in query:
                    # перебираем ключи
                    # и если они совпадают добовляем
                    matching_keys.update(cnt_2)
        return matching_keys

    # Предложения по назначению ID-шников(Оля). После номеров класса стоит добавлять время в микросекудах. Таким
    # образом мы получим айдишник, который можно будет понимать и без словаря обозначений. Например экземпляр класса
    # location может быть записан по ID, как 04412494(где 04- код класса, а 412494- микросекунды в момент записи ID).
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
            # new cтроку 96-99 перенести выше виз опена; папка дб берется из файл сорса как файл паз ВЕЗДЕ!!!!
            current_records = self.__read_json_db(collection_name)
            document["object_id"] = int(str(self.dictionary[collection_name]) + str(FileSource.generate_id()))
            current_records.append(document)
            target_json = self.__class__.serialize_records_to_json(current_records)
            data_file.write(target_json)
        return document  # new возвращаем получаемый файл

    def update(self, collection_name: str, object_id: int, document: dict) -> dict:
        with open(f"./db/{collection_name}.json", mode="w", encoding='utf-8') as data_file:
            current_records = self.__read_json_db(collection_name)
            for i in current_records:
                if i["object_id"] == object_id:
                    # new проверять, есть ли обжект айди в документе
                    new_dict = i
                    new_dict.update(document)
                    current_records.remove(current_records.index(i))
                    current_records.append(new_dict)
            target_json = self.__class__.serialize_records_to_json(current_records)
            data_file.write(target_json)
        return new_dict  # new возвращаем новый объект

    def delete(self, collection_name: str, object_id: int) -> dict:
        # new все перенести из виз опена сюда и начальную папку брать из данных выше
        with open(f"./db/{collection_name}.json", mode="w", encoding='utf-8') as data_file:
            current_records = self.__read_json_db(collection_name)
            for i in current_records:
                if i["object_id"] == object_id:
                    current_records.remove(current_records.index(i))
            target_json = self.__class__.serialize_records_to_json(current_records)
            data_file.write(target_json)
        return {None: None}  # new удаленный объект без обжект айди

    # __read_json_db подвергся некоторым изменениям, в частности на ввод был добавлен аргумент collection_name- он
    # принимает имя файла, чтобы данную функцию стало возможно применять для любого класса
    @classmethod  # NEW убрать класс методы
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

    @staticmethod
    def generate_id():
        return datetime.microsecond
