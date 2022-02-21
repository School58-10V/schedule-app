from typing import List
import psycopg2
from psycopg2 import errorcodes


class DBSource:
    """
        Адаптер для работы с базой данных
    """

    def __init__(self, host, user, password, dbname='schedule_app'):
        conn = psycopg2.connect(
            dbname=dbname, user=user,
            password=password, host=host
        )
        self.__conn = conn
        self.__cursor = conn.cursor()

    def get_by_query(self, collection_name: str, query: dict) -> List[dict]:
        pass

    def get_all(self, collection_name: str) -> List[dict]:
        request = f'SELECT * FROM "{collection_name}"'
        self.__cursor.execute(request)
        data = self.__cursor.fetchall()
        desc = self.__cursor.description

        return self.__format_tuple_to_dict(data, desc)

    def get_by_id(self, collection_name: str, object_id: int) -> dict:
        request = f'SELECT * FROM "{collection_name}" WHERE object_id={object_id}'
        self.__cursor.execute(request)
        data = self.__cursor.fetchall()
        desc = self.__cursor.description
        if len(data) == 0:
            raise ValueError(f'Объект с id {object_id} из {collection_name} не существует')
        # берем 0 индекс т.к. длина ответа всегда либо 0 (уже обработали), либо 1, т.е. смысла возвращать список нет.
        return self.__format_tuple_to_dict(data, desc)[0]

    def check_unique_id(self, collection_name: str, object_id: int) -> bool:
        pass

    def insert(self, collection_name: str, document: dict) -> dict:
        try:
            self.__cursor.execute(f'SELECT * FROM "{collection_name}s" LIMIT 0')
        except psycopg2.Error as e:
            if errorcodes.lookup(e.pgcode) == 'UNDEFINED_TABLE':
                raise ValueError('Данной таблицы не существует.')
        desc = [x[0] for x in self.__cursor.description]
        values = [f'\'{document[x]}\'' if x != 'object_id' else 'default' for x in desc]
        request = f'INSERT INTO "{collection_name}s" VALUES ({",".join(map(str, values))});'
        try:
            self.__cursor.execute(request)
        except psycopg2.Error as e:
            if errorcodes.lookup(e.pgcode) == 'UNIQUE_VIOLATION':
                raise ValueError('ID добавляемого объекта уже существует.')
            elif errorcodes.lookup(e.pgcode) == 'FOREIGN_KEY_VIOLATION':
                raise ValueError('Один из ID связанных объектов недействителен.')
            elif errorcodes.lookup(e.pgcode) == 'INVALID_TEXT_REPRESENTATION':
                raise TypeError('Ошибка в типах данных.')
            raise ValueError(f"Неизвестная ошибка при добавлении новой записи в {collection_name}. Код ошибки: {errorcodes.lookup(e.pgcode)}")
        self.__conn.commit()
        return document

    def update(self, collection_name: str, object_id: int, document: dict) -> dict:
        pass

    def delete(self, collection_name: str, object_id: int) -> dict:
        pass

    @classmethod
    def __format_tuple_to_dict(cls, data, desc):
        # data - список значений
        # desc - список имен полей
        # используя data и desc, полученных из cursor, мы их соединяем и получаем словарь с данными
        to_return = []
        for i in data:
            to_return.append({desc[j].name: i[j] for j in range(len(desc))})
        return to_return

