from __future__ import annotations
import time
import datetime
from adapters.abstract_source import AbstractSource
from typing import List, Optional, Tuple
import psycopg2
from psycopg2 import errorcodes
from loguru import logger


class DBSource(AbstractSource):
    """
        Адаптер для работы с базой данных
    """

    def __init__(self, host, user, password, dbname='schedule_app', options="-c search_path=dbo,public"):
        self.__connection_data = {"host": host, "user": user, "password": password,
                                  "dbname": dbname, "options": options}
        self.__conn = None
        logger.info(f"Инициализирован DBSource на адресe '{host}' по пользователю '{user}' с настройками {options}.")

    def connect(self, retry_count: int = 3):
        if self.__conn:
            return
        for i in range(retry_count):
            logger.info(f"Попытка подключения к базе #{i + 1} по адресу {self.__connection_data['host']}.")
            state = False
            try:
                self.__conn = psycopg2.connect(**self.__connection_data)
                state = True
                # cursor_factory=DictCursor
                # это можно добавить чтобы курсор работал со словарями вместо кортежей,
                # но я не стал добавлять его сразу
                break
            except psycopg2.Error:
                time.sleep(5)
        if state:
            logger.info("Успешное подключение к базе!")
        else:
            logger.error("Произошла ошибка при подключении к базе, превышено кол-во попыток!")

    def get_by_query(self, collection_name: str, query: dict) -> List[dict]:
        logger.debug(f"Начинаю поиск по квери в коллекции '{collection_name}'...")
        curr_time = time.time_ns()
        self.connect()
        pairs = query.items()
        request = f'SELECT * FROM "{collection_name}" WHERE '
        request += ' AND '.join([f'{i[0]}=\'{i[1]}\'' for i in pairs])
        cursor = self.__conn.cursor()
        self.__cursor_execute_wrapper(cursor, request, list(query.values()))
        data = cursor.fetchall()
        desc = cursor.descriptio

        logger.debug(f"Поиск завершён, времени затрачено: {(time.time_ns() - curr_time) / 1000000}!")
        return self.__format_Tuple_to_dict(data, desc)

    def run_query(self, query):
        self.connect()
        cursor = self.__conn.cursor()
        self.__cursor_execute_wrapper(cursor, query)
        data = cursor.fetchall()
        self.__conn.commit()

        return data

    def get_all(self, collection_name: str) -> List[dict]:
        logger.debug(f"Собираю все данные из коллекции '{collection_name}'...")
        curr_time = time.time_ns()
        self.connect()
        request = f'SELECT * FROM "{collection_name}"'
        cursor = self.__conn.cursor()
        self.__cursor_execute_wrapper(cursor, request)
        data = cursor.fetchall()
        desc = cursor.description
        self.__conn.commit()

        logger.debug(f"Сбор данных из коллекции {collection_name} завершён, времени затрачено: {(time.time_ns() - curr_time) / 1000000}!")
        return self.__format_Tuple_to_dict(data, desc)

    def get_by_id(self, collection_name: str, object_id: int) -> dict:
        logger.debug(f"Ищу данные по id {object_id} в коллекции '{collection_name}'...")
        curr_time = time.time_ns()
        self.connect()
        request = f'SELECT * FROM "{collection_name}" WHERE object_id={object_id}'
        cursor = self.__conn.cursor()
        self.__cursor_execute_wrapper(cursor, request)
        data = cursor.fetchall()
        desc = cursor.description
        if len(data) == 0:
            logger.error(f'Объекта с id {object_id} из {collection_name} не существует!')
            self.__conn.commit()
            raise ValueError(f'Объект с id {object_id} из {collection_name} не существует')
        # берем 0 индекс т.к. длина ответа всегда либо 0 (уже обработали), либо 1, т.е. смысла возвращать список нет.

        logger.debug(f"Поиск объекта завершён, времени затрачено: {(time.time_ns() - curr_time) / 1000000}!")
        return self.__format_Tuple_to_dict(data, desc)[0]

    def insert(self, collection_name: str, document: dict) -> dict:
        logger.debug(f"Добавляю новый объект в коллекцию '{collection_name}'...")
        curr_time = time.time_ns()
        self.connect()
        cursor = self.__conn.cursor()
        try:
            cursor.execute(f'SELECT * FROM "{collection_name}" LIMIT 0')
        except psycopg2.Error as e:
            logger.error(f"При добавлении объекта в коллекцию {collection_name} произошла ошибка {e}!")
            if errorcodes.lookup(e.pgcode) == 'UNDEFINED_TABLE':
                self.__conn.commit()
                raise ValueError('Данной таблицы не существует.')

        desc = [x[0] for x in cursor.description]
        values = [self.__wrap_string(document[x]) if x != 'object_id' else 'default' for x in desc]
        request = f'INSERT INTO "{collection_name}" VALUES ({",".join(map(str, values))}) RETURNING *;'
        try:
            cursor.execute(request)
        except psycopg2.Error as e:
            logger.error(f"При добавлении объекта в коллекцию {collection_name} произошла ошибка {e}!")
            self.__conn.commit()
            if errorcodes.lookup(e.pgcode) == 'UNIQUE_VIOLATION':
                raise ValueError('ID добавляемого объекта уже существует.')
            elif errorcodes.lookup(e.pgcode) == 'FOREIGN_KEY_VIOLATION':
                raise ValueError('Один из ID связанных объектов недействителен.')
            elif errorcodes.lookup(e.pgcode) == 'INVALID_TEXT_REPRESENTATION':
                raise TypeError('Ошибка в типах данных.')
            raise ValueError(f"Неизвестная ошибка при добавлении новой записи в {collection_name}. "
                             f"Код ошибки: {errorcodes.lookup(e.pgcode)}")
        self.__conn.commit()
        new_obj = cursor.fetchone()
        new_doc = {desc[index]: new_obj[index] for index in range(len(desc))}

        logger.debug(f"Добавление объекта завершено, времени затрачено: {(time.time_ns() - curr_time) / 1000000}!")
        return new_doc

    def update(self, collection_name: str, object_id: Optional[int, str], document: dict) -> dict:
        logger.debug(f"Обновляю объект по id {object_id} в коллекции '{collection_name}'...")
        curr_time = time.time_ns()
        self.connect()
        cursor = self.__conn.cursor()
        document.pop('object_id')
        collection = collection_name
        req_data = []
        # TODO: remove this if statement, shouldn't be required
        if not collection_name.endswith("s"):
            collection += "s"
        for elem in document:
            req_data.append(f"{elem} = {self.__wrap_string(document.get(elem))}")
        try:
            request = f'UPDATE "{collection}" SET {", ".join(req_data)} WHERE object_id = {str(object_id)}'
            cursor.execute(request)
            self.__conn.commit()
            logger.debug(f"Успешно обновлён объект по id {object_id}, времени затрачено {(time.time_ns() - curr_time) / 1000000}!")
            return document
        except psycopg2.Error as e:
            logger.error(f"При обновлении объекта по id {object_id} из коллекции {collection_name} произошла ошибка {e}!")

    def delete(self, collection_name: str, object_id: Optional[int, str]):
        logger.debug(f"Удаляю объект по id {object_id} в коллекции '{collection_name}'...")
        curr_time = time.time_ns()
        self.connect()
        cursor = self.__conn.cursor()

        collection = collection_name
        if not collection_name.endswith("s"):
            collection += "s"
        request = f'DELETE FROM "{collection}" WHERE object_id = {object_id}'
        try:
            cursor.execute(request)
            self.__conn.commit()
            logger.debug(f"Успешно удалён объект по id {object_id}, времени затрачено {(time.time_ns() - curr_time) / 1000000}!")
        except psycopg2.Error as e:
            logger.error(f"Произошла ошибка {e} при удалении объекта по id {object_id} из коллекции {collection_name}!")

    @staticmethod
    def __wrap_string(value: Optional[str]) -> str:
        if value is None:
            # Для базы None записывается по-другому
            return 'null'
        elif type(value) == str or type(value) == datetime.date:
            # Дата и строки должны быть в ковычках
            return f"'{value}'"
        else:
            return value

    def __data_processing(self, document: dict) -> Tuple[str, str]:
        # Функция, которая преобразовывает данные моделей для запроса
        # (для добавление этой модели в базу данных)
        lst1 = []
        lst2 = []
        for i in document:
            if i != 'object_id':
                # id в базе данных не нужен, он генерируется сам
                lst1.append(i)
                if document[i] is None:
                    # Для базы None записывается по-другому
                    lst2.append('null')
                elif type(document[i]) == str or type(document[i]) == datetime.date:
                    # Дата и строки должны быть в ковычках
                    lst2.append(f"'{document[i]}'")
                else:
                    # А остальное вроде как нет (интересно, что сюда кроме int попадет...)
                    lst2.append(str(document[i]))
        # Возвращаем две строки - названия колонок и соответствующие значения
        return ", ".join(lst1), ", ".join(lst2)

    @classmethod
    def __format_Tuple_to_dict(cls, data: list, desc: list) -> list[dict]:
        # data - список значений
        # desc - список имен полей
        # используя data и desc, полученных из cursor, мы их соединяем и получаем словарь с данными
        to_return = []
        for i in data:
            to_return.append({desc[j].name: i[j] for j in range(len(desc))})
        return to_return

    @classmethod
    def __cursor_execute_wrapper(cls, cursor: any, request: str, params=None):
        try:
            cursor.execute(request, params)
        except psycopg2.Error as e:
            if errorcodes.lookup(e.pgcode) == 'UNDEFINED_TABLE':
                raise ValueError(f'Ошибка во время выполнения запроса, таблица не существует. Запрос: {request}')
            else:
                # why print here??
                print(e)
                raise ValueError(f'Неизвестная ошибка во время выполнения запроса, '
                                 f'код ошибки: {errorcodes.lookup(e.pgcode)}. Запрос: {request}')
