from __future__ import annotations
import time
import datetime
from adapters.abstract_source import AbstractSource
from typing import List, Optional, Tuple
import psycopg2
from psycopg2 import errorcodes
import logging
from services.logger.messages_templates import MessagesTemplates


LOGGER = logging.getLogger("main.adapter")
MESSAGES = MessagesTemplates()

class DBSource(AbstractSource):
    """
        Адаптер для работы с базой данных
    """

    def __init__(self, host, user, password, dbname='schedule_app', options="-c search_path=dbo,public"):
        self.__connection_data = {"host": host, "user": user, "password": password,
                                  "dbname": dbname, "options": options}
        self.__conn = None
        LOGGER.info(f"Created db_source on '{host}' with user: '{user}' with options: {options}.")

    def connect(self, retry_count: int = 3):
        if self.__conn:
            return
        for i in range(retry_count):
            LOGGER.info(f"DB connection attempt #{i + 1} on adress {self.__connection_data['host']}.")
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
            LOGGER.info(MESSAGES.Adapter.Success.get_connection())
        else:
            LOGGER.error(MESSAGES.Adapter.Error.get_connection())

    def get_by_query(self, collection_name: str, query: dict) -> List[dict]:
        LOGGER.debug(MESSAGES.Adapter.Start.get_query_search(collection_name, query))
        curr_time = time.time_ns()
        self.connect()
        pairs = query.items()
        request = f'SELECT * FROM "{collection_name}" WHERE '
        request += ' AND '.join([f'{i[0]}=\'{i[1]}\'' for i in pairs])
        cursor = self.__conn.cursor()
        self.__cursor_execute_wrapper(cursor, request, list(query.values()))
        data = cursor.fetchall()
        desc = cursor.description

        LOGGER.debug(MESSAGES.Adapter.Success.get_query_search((time.time_ns() - curr_time) / 1000000))
        return self.__format_Tuple_to_dict(data, desc)

    def run_query(self, query):
        self.connect()
        cursor = self.__conn.cursor()
        curr_time = time.time_ns()
        LOGGER.debug(MESSAGES.Adapter.Start.get_custom_query(query))
        self.__cursor_execute_wrapper(cursor, query)
        data = cursor.fetchall()
        self.__conn.commit()
        LOGGER.debug(MESSAGES.Adapter.Success.get_custom_query((time.time_ns() - curr_time) / 1000000))

        return data

    def get_all(self, collection_name: str) -> List[dict]:
        LOGGER.debug(MESSAGES.Adapter.Start.get_collect_all(collection_name))
        curr_time = time.time_ns()
        self.connect()
        request = f'SELECT * FROM "{collection_name}"'
        cursor = self.__conn.cursor()
        self.__cursor_execute_wrapper(cursor, request)
        data = cursor.fetchall()
        desc = cursor.description
        self.__conn.commit()

        LOGGER.debug(MESSAGES.Adapter.Success.get_collect_all(collection_name, (time.time_ns() - curr_time) / 1000000))
        return self.__format_Tuple_to_dict(data, desc)

    def get_by_id(self, collection_name: str, object_id: int) -> dict:
        LOGGER.debug(MESSAGES.Adapter.Start.get_find_by_id(object_id, collection_name))
        curr_time = time.time_ns()
        self.connect()
        request = f'SELECT * FROM "{collection_name}" WHERE object_id={object_id}'
        cursor = self.__conn.cursor()
        self.__cursor_execute_wrapper(cursor, request)
        data = cursor.fetchall()
        desc = cursor.description
        if len(data) == 0:
            LOGGER.error(MESSAGES.General.get_id_not_found_message(collection_name, object_id))
            self.__conn.commit()
            raise ValueError(f'Object with id {object_id} does not exist in {collection_name}!')
        # берем 0 индекс т.к. длина ответа всегда либо 0 (уже обработали), либо 1, т.е. смысла возвращать список нет.

        LOGGER.debug(MESSAGES.Adapter.Success.get_find_by_id((time.time_ns() - curr_time) / 1000000))
        return self.__format_Tuple_to_dict(data, desc)[0]

    def insert(self, collection_name: str, document: dict) -> dict:
        LOGGER.debug(MESSAGES.Adapter.Start.get_insert(collection_name, document))
        curr_time = time.time_ns()
        self.connect()
        cursor = self.__conn.cursor()
        try:
            cursor.execute(f'SELECT * FROM "{collection_name}" LIMIT 0')
        except psycopg2.Error as e:
            LOGGER.error(MESSAGES.Adapter.Error.get_insert(errorcodes.lookup(e.pgcode), collection_name))
            if errorcodes.lookup(e.pgcode) == 'UNDEFINED_TABLE':
                self.__conn.commit()
                raise ValueError('This table does not exist!')

        desc = [x[0] for x in cursor.description]
        values = [self.__wrap_string(document[x]) if x != 'object_id' else 'default' for x in desc]
        request = f'INSERT INTO "{collection_name}" VALUES ({",".join(map(str, values))}) RETURNING *;'
        try:
            cursor.execute(request)
        except psycopg2.Error as e:
            LOGGER.error(MESSAGES.Adapter.Error.get_insert(errorcodes.lookup(e.pgcode), collection_name))
            self.__conn.commit()
            error_text = ""
            if errorcodes.lookup(e.pgcode) == 'UNIQUE_VIOLATION':
                error_text = 'Object with this id already exists!'
            elif errorcodes.lookup(e.pgcode) == 'FOREIGN_KEY_VIOLATION':
                error_text = 'One of the connected IDs is invalid!'
            elif errorcodes.lookup(e.pgcode) == 'INVALID_TEXT_REPRESENTATION':
                error_text = 'Object data type error'
            
            if error_text != "":
                LOGGER.error(MESSAGES.Adapter.Error.get_insert(error_text, collection_name))
                raise ValueError(error_text)
            else:
                LOGGER.error(MESSAGES.Adapter.Error.get_insert({errorcodes.lookup(e.pgcode)}, collection_name))
                raise ValueError(f"Encountered an unknown error while adding an object to {collection_name}. "
                             f"Error code: {errorcodes.lookup(e.pgcode)}")
        self.__conn.commit()
        new_obj = cursor.fetchone()
        new_doc = {desc[index]: new_obj[index] for index in range(len(desc))}

        LOGGER.debug(MESSAGES.Adapter.Success.get_insert((time.time_ns() - curr_time) / 1000000))
        return new_doc

    def update(self, collection_name: str, object_id: Optional[int, str], document: dict) -> dict:
        LOGGER.debug(MESSAGES.Adapter.Start.get_update(object_id, collection_name))
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
            LOGGER.debug(MESSAGES.Adapter.Success.get_update(object_id, (time.time_ns() - curr_time) / 1000000))
            return document
        except psycopg2.Error as e:
            LOGGER.error(MESSAGES.Adapter.Error.get_update(e, object_id, collection_name))

    def delete(self, collection_name: str, object_id: Optional[int, str]):
        LOGGER.debug(MESSAGES.Adapter.Start.get_delete(object_id, collection_name))
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
            LOGGER.debug(MESSAGES.Adapter.Success.get_delete(object_id, (time.time_ns() - curr_time) / 1000000))
        except psycopg2.Error as e:
            LOGGER.error(MESSAGES.Adapter.Error.get_delete(e, object_id, collection_name))

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
                LOGGER.error(f"Encountered an error while processing a request {request}! Specified table does not exist!")
                raise ValueError(f"Encountered an error while processing a request {request}! Specified table does not exist!")
            else:
                LOGGER.error(f"Encountered an unknown error while processing a request {request}. Errorcode: {errorcodes.lookup(e.pgcode)}")
                raise ValueError(f"Encountered an unknown error while processing a request {request}. Errorcode: {errorcodes.lookup(e.pgcode)}")
