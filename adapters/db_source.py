import datetime
from typing import List
import psycopg2
from psycopg2 import errorcodes


class DBSource:
    """
        Адаптер для работы с базой данных
    """

    def __init__(self, host, user, password, dbname='schedule_app'):
        try:
            conn = psycopg2.connect(
                dbname=dbname, user=user,
                password=password, host=host
            )
        except psycopg2.Error:
            raise ValueError('Ошибка во время подключения к базе данных!')
        self.__conn = conn

    def get_by_query(self, collection_name: str, query: dict) -> List[dict]:
        pairs = query.items()
        request = f'SELECT * FROM "{collection_name}" WHERE '
        for i in pairs:
            request += f'{i[0]}={i[1]} and '
        cursor = self.__conn.cursor()
        print(request)
        self.__cursor_execute_wrapper(cursor, request, list(query.values()))
        data = cursor.fetchall()
        desc = cursor.description

        # if len(data) == 0:
        #     raise ValueError(f'Объект где {", ".join([str(i[0]) + "=" + str(i[1]) for i in pairs])} не существует.')

        return self.__format_tuple_to_dict(data, desc)

    def get_all(self, collection_name: str) -> List[dict]:
        request = f'SELECT * FROM "{collection_name}"'
        cursor = self.__conn.cursor()
        self.__cursor_execute_wrapper(cursor, request)
        data = cursor.fetchall()
        desc = cursor.description

        return self.__format_tuple_to_dict(data, desc)

    def get_by_id(self, collection_name: str, object_id: int) -> dict:
        request = f'SELECT * FROM "{collection_name}" WHERE object_id={object_id}'
        cursor = self.__conn.cursor()
        self.__cursor_execute_wrapper(cursor, request)
        data = cursor.fetchall()
        desc = cursor.description
        if len(data) == 0:
            raise ValueError(f'Объект с id {object_id} из {collection_name} не существует')
        # берем 0 индекс т.к. длина ответа всегда либо 0 (уже обработали), либо 1, т.е. смысла возвращать список нет.
        return self.__format_tuple_to_dict(data, desc)[0]

    def check_unique_id(self, collection_name: str, object_id: int) -> bool:
        pass

    def insert(self, collection_name: str, document: dict) -> dict:  # назначение айди надо будет вынести в общий класс
        # ФАНФАКТ: psycopg2.errors.NumericValueOutOfRange: value "1011645028399052" is out of range for type integer
        self.__cursor.execute(f'SELECT * FROM "{collection_name}s" LIMIT 0')  # делаем пустой запрос, чтобы обратиться к таблице
        desc = [x[0] for x in self.__cursor.description]  # получаем столбцы таблицы (чтобы потом передать данные в нужном порядке)
        values = [f'\'{document[x]}\'' for x in desc]  # записываем все нужные нам данные из документа
        request = f'INSERT INTO "{collection_name}s" VALUES ({",".join(map(str, values))});'
        self.__cursor.execute(request)  # выполняем запрос
        self.__conn.commit()  # сохраняем изменения в базе
        return document  # ??? не знаю, что возвращать на самом дел

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
      
    @classmethod
    def __cursor_execute_wrapper(cls, cursor, request, params=None):
        try:
            cursor.execute(request, params)
        except psycopg2.Error as e:
            if errorcodes.lookup(e.pgcode) == 'UNDEFINED_TABLE':
                raise ValueError(f'Ошибка во время выполнения запроса, таблица не существует. Запрос: {request}')
            else:
                raise ValueError(f'Неизвестная ошибка во время выполнения запроса, '
                                 f'код ошибки: {errorcodes.lookup(e.pgcode)}. Запрос: {request}')

