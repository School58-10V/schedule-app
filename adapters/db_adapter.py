import time

import psycopg2
from psycopg2.extras import DictCursor


class DbAdapter:
    def __init__(self):
        self.__connection = None
        self.__cursor = None
        self.start_adapter()

    def start_adapter(self):
        try:
            self.__connection = psycopg2.connect(dbname='schedule_app', user='schedule_app',
                                                 password='VYRL!9XEB3yXQs4aPz_Q', host='postgresql.aakapustin.ru')
            self.__cursor = self.__connection.cursor(cursor_factory=DictCursor)
            print("Успешное подключение к базе!")
        except Exception:
            print("Невозможно подключиться к базе, проверьте данные!")
            time.sleep(5)
            self.start_adapter()

    def update(self, collection_name: str, data: dict):
        object_id = data.pop("object_id")
        collection = collection_name
        if self.__connection is None:
            self.start_adapter()
        if not collection_name.endswith("s"):
            collection += "s"
        for i in range(len(data)):
            key = self.get_key(data, i)
            request = f'UPDATE "{collection}" SET {str(key)} = {str(data.get(key))} WHERE object_id = {str(object_id)}'
            print(request)
            self.__cursor.execute(request)
        return data

    @staticmethod
    def get_key(data: dict, iterator: int):
        counter = -1
        for key in data:
            counter += 1
            if counter == iterator:
                return key
        return None
