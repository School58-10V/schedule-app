from __future__ import annotations  # нужно чтобы parse мог быть типизирован

import json

from data_model.abstract_model import AbstractModel
from typing import Optional, List


class Teacher(AbstractModel):
    """
        Класс учителя.
        fio - ФИО
        object_id - ид учителя
        bio - инфа о учителе
        contacts - Контакты учителя
        office_id - закреплённый кабинет
        subject - его предмет.
    """

    def __init__(self, fio: str, subject: str, object_id: Optional[int] = None, 
                 office_id: int = None, bio: str = None,
                 contacts: str = None):
        self.__fio = fio
        self._object_id = object_id
        self.__bio = bio
        self.__contacts = contacts
        self.__office_id = office_id
        self.__subject = subject

    def get_fio(self) -> str:
        return self.__fio

    def get_bio(self) -> Optional[str]:
        return self.__bio

    def get_contacts(self) -> Optional[str]:
        return self.__contacts

    def get_subject(self) -> str:
        return self.__subject

    def get_office_id(self) -> Optional[int]:
        return self.__office_id

    @staticmethod
    def parse(file_location) -> List[(Optional[str], Optional[Teacher])]:
        with open(file_location, encoding='utf-8') as f:
            lines = [i.split(';') for i in f.read().split('\n')[1:]]
            res = []

            for i in lines:
                try:
                    fio = i[0]
                    subject = i[1]
                    office_id = int(i[2])
                    bio = i[3]
                    contacts = i[4]

                    res.append((None, Teacher(fio=fio, subject=subject, 
                                              office_id=office_id, bio=bio, 
                                              contacts=contacts, object_id=None)))
                except IndexError as e:
                    exception_text = f"Строка {lines.index(i) + 1} не добавилась в [res]"
                    print(exception_text)
                    print(e)
                    res.append((exception_text, None))
                except Exception as e:
                    exception_text = f"Неизвестная ошибка в Teacher.parse():\n{e}"
                    print(exception_text)
                    res.append((exception_text, None))
        return res

    def __dict__(self) -> dict:
        return {"fio": self.__fio,
                "object_id": self._object_id,
                "bio": self.__bio,
                "contacts": self.__contacts,
                "office_id": self.__office_id,
                "subject": self.__subject}

    def __str__(self):
        return f'Teacher(fio = {self.__fio}, subject = {self.__subject}, bio = {self.__bio}, ' \
               f'contacts =  {self.__contacts}) '

    def get_all_lesson_row(self, db_path: str = './db') -> list[int]:
        """
            Читает файл сохранения TeachersOnLessonRows и достает от
            туда id всех урокой учителя с данным object_id
            :param db_path: путь до папки с .json файлами
            :return: список с id уроков
        """
        lst_lessons = []
        file_lesson = []
        try:
            # Открываем и читаем файл TeachersOnLessonRows
            with open(f'{db_path}/TeachersOnLessonRows.json', encoding='utf-8') as file:
                file_lesson = json.loads(file.read())
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            # Если файла нет или он пустой, то выдаем ошибку
            raise FileNotFoundError('Файл не найден')

        # lst_lesson = [i['lesson_row_id'] for i in file_lesson if i['teacher_id'] == self._object_id]
        for i in file_lesson:
            # Пробегаемся циклом по списку  и находим
            # там данные об объектах, где есть учитель на ряд
            # уроков с таким же id, как и у нашего объекта
            if i['teacher_id'] == self._object_id:
                # Если он есть, добавляем id его урока в список, который будем возвращать
                lst_lessons.append(i['lesson_row_id'])
        return lst_lessons
