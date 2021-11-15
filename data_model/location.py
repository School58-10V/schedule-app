from __future__ import annotations  # нужно чтобы parse мог быть типизирован
import json

from typing import Optional, List

from data_model.abstract_model import AbstractModel


class Location(AbstractModel):
    """
                      ID - Идентификационный номер места проведения урока
            num_of_class - номер класса, в котором проходит занятие
                 Profile - профиль класса(например "хим.", если кабинет оборудован для уроков химии)
               Equipment - оборудование в классе
                    Link - на случай дистанта ссылка(в Сибирь) для подключения к месту проведения урока
        type_of_location - Тип локации- класс, поточная аудитория, видеоконференция и т.д.
    """

    def __init__(self, type_of_location: str, object_id: int = None, location_desc: str = None, profile: str = None,
                 equipment: list = None, link: str = 'Offline', comment: str = ''):
        self.__object_id = object_id
        self.__location_desc = location_desc
        self.__profile = profile
        self.__equipment = equipment
        self.__link = link
        self.__type_of_location = type_of_location
        self.__comment = comment

    def get_location_desc(self):
        return self.__location_desc

    def get_profile(self):
        return self.__profile

    def get_equipment(self):
        return self.__equipment

    def get_link(self):
        return self.__link

    def get_type_of_location(self):
        return self.__type_of_location

    def get_comment(self):
        return self.__comment

    @staticmethod
    def parse(file_location) -> List[(Optional[str], Optional[Location])]:
        f = open(file_location, encoding='utf-8')
        lines = f.read().split('\n')[1:]
        lines = [i.split(';') for i in lines]
        res = []

        for i in lines:
            try:
                location_type = i[0]
                name = i[1]
                link = i[2]
                comment = i[3]
                res.append((None, Location(location_type, link=link,
                                           location_desc=name if name.isdigit() else None, comment=comment)))
            except IndexError as e:
                exception_text = f"Строка {lines.index(i) + 2} не добавилась в [res]"
                print(exception_text)
                print(e)
                res.append((exception_text, None))
            except Exception as e:
                exception_text = f"Неизвестная ошибка в Location.parse():\n{e}"
                print(exception_text)
                res.append((exception_text, None))

        return res

    def __str__(self):
        return f'Location(type_of_location={self.__type_of_location}, name={self.__location_desc}, ' \
               f'link={self.__link}, comment={self.__comment})'

    def __dict__(self):
        return {'object_id': self.__object_id,
                'location_desc': self.__location_desc,
                'profile': self.__profile,
                'equipment': self.__equipment,
                'link': self.__link,
                'type_of_location': self.__type_of_location,
                'comment': self.__comment}
