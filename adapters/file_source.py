import json


class FileSource:
    def __init__(self, dp_path: str = './db'):
        self.__dp_path = dp_path

    def __dp_path(self):
        return self.__dp_path

# Метод get_all принимает имя коллекции и возвращает все объекты коллекции в представлении Python(напр. все объеты
# класса Location можно получить, если использовать get_all("Location"))
    @classmethod
    def get_all(cls, collection_name: str) -> list[dict]:
        return [cls(**i) for i in cls.__read_json_db(cls.__dp_path(), collection_name)]

    @classmethod
    def get_by_id(cls, collection_name: str, element_id: int) -> dict:
        for i in cls.__read_json_db(cls.__dp_path(), collection_name):
            if i['group_id'] == element_id:
                return cls(**i)

    def get_by_query(self, collection_name: str, query: dict[str, Any]) -> list[dict]:
        pass

    def insert(self, collection_name: str, document: dict) -> dict:
        pass

    def update(self, collection_name: str, elem_id: int, document: dict) -> dict:
        pass

    def delete(self, collection_name: str, elem_id: int) -> dict:
        pass

# __read_json_db подвергся некоторым изменениям, в частности на ввод был добавлен аргумент collection_name- он
# принимает имя файла, чтобы данную функцию стало возможно применять для любого класса.
    @classmethod
    def __read_json_db(cls, db_path, collection_name) -> list:
        try:
            with open(f"{db_path}/{collection_name}.json",
                      mode="r", encoding='utf-8') as data_file:
                record = json.loads(data_file.read())
                return record
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return []
