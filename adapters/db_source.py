import datetime

from adapters.abstract_source import AbstractSource
from typing import List
import psycopg2


class DBSource(AbstractSource):
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
        request = f'SELECT * FROM "{collection_name}s"'
        self.__cursor.execute(request)
        data = self.__cursor.fetchall()
        desc = self.__cursor.description

        return self.__format_tuple_to_dict(data, desc)

    def get_by_id(self, collection_name: str, object_id: int) -> dict:
        if object_id is None:
            raise ValueError("Ошибка с id: id не может быть None")
        request = f'SELECT * FROM "{collection_name}s" WHERE object_id={object_id}'
        self.__cursor.execute(request)
        data = self.__cursor.fetchall()
        desc = self.__cursor.description
        if len(data) == 0:
            raise ValueError(f'Объект с id {object_id} из {collection_name} не существует')
        # берем 0 индекс т.к. длина ответа всегда либо 0 (уже обработали), либо 1, т.е. смысла возвращать список нет.
        return self.__format_tuple_to_dict(data, desc)[0]

    def check_unique_id(self, collection_name: str, object_id: int) -> bool:
        pass

    # def insert(self, collection_name: str, document: dict) -> dict:  # назначение айди надо будет вынести в общий
    # класс ФАНФАКТ: psycopg2.errors.NumericValueOutOfRange: value "1011645028399052" is out of range for type
    # integer self.__cursor.execute( f'SELECT * FROM "{collection_name}s" LIMIT 0')  # делаем пустой запрос,
    # чтобы обратиться к таблице desc = [x[0] for x in self.__cursor.description]  # получаем столбцы таблицы (чтобы
    # потом передать данные в нужном порядке) values = [f'\'{document[x]}\'' for x in desc]  # записываем все нужные
    # нам данные из документа

    def insert(self, collection_name: str, document: dict) -> dict:
        column, value = self.__data_processing(document)  # Берем обработанные для запроса данные
        request = f'INSERT INTO "{collection_name}s"({column}) VALUES ({value});'  # Генерируем запрос
        print(request)
        self.__cursor.execute(request)  # выполняем запрос
        self.__conn.commit()  # сохраняем изменения в базе
        return document

    def update(self, collection_name: str, object_id: int, document: dict) -> dict:
        pass

    def delete(self, collection_name: str, object_id: int) -> dict:
        pass

    def __data_processing(self, document):
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
    def __format_tuple_to_dict(cls, data, desc):
        # data - список значений
        # desc - список имен полей
        # используя data и desc, полученных из cursor, мы их соединяем и получаем словарь с данными
        to_return = []
        for i in data:
            to_return.append({desc[j].name: i[j] for j in range(len(desc))})
        return to_return
