from __future__ import annotations  # нужно чтобы parse мог быть типизирован
import json
from data_model.parsed_data import ParsedData
from typing import Optional, List, TYPE_CHECKING

from data_model.abstract_model import AbstractModel

if TYPE_CHECKING:
    from adapters.file_source import FileSource


class Location(AbstractModel):
    """
                      ID - Идентификационный номер места проведения урока
            num_of_class - номер класса, в котором проходит занятие
                 Profile - профиль класса(например "хим.", если кабинет оборудован для уроков химии)
               Equipment - оборудование в классе
                    Link - на случай дистанта ссылка(в Сибирь) для подключения к месту проведения урока
        location_type - Тип локации- класс, поточная аудитория, видеоконференция и т.д.
    """

    def __init__(self, db_source: FileSource, location_type: str, object_id: int = None,
                 location_desc: str = None, profile: str = None, num_of_class: int = None,
                 equipment: list = None, link: str = 'Offline', comment: str = ''):
        super().__init__(db_source)
        self.__location_type = location_type
        self._object_id = object_id
        self.__location_desc = location_desc
        self.__profile = profile
        self.__num_of_class = num_of_class
        self.__equipment = equipment
        self.__link = link
        self.__comment = comment

    def get_location_desc(self) -> str:
        return self.__location_desc

    def get_profile(self) -> str:
        return self.__profile

    def get_num_of_class(self) -> int:
        return self.__num_of_class

    def get_equipment(self) -> list:
        return self.__equipment

    def get_link(self) -> str:
        return self.__link

    def get_location_type(self) -> str:
        return self.__location_type

    def get_comment(self) -> str:
        return self.__comment

    @staticmethod
    def parse(file_location, db_source: FileSource) -> List[(Optional[str], Optional[Location])]:
        f = open(file_location, encoding='utf-8')
        lines = f.read().split('\n')[1:]
        lines = [i.split(';') for i in lines]
        res = []

        for i in lines:
            try:
                location_type = i[0]
                num_of_class = int(i[1])
                link = i[2]
                comment = i[3]
                res.append(ParsedData(None, Location(db_source, location_type, link=link,
                                                     num_of_class=num_of_class, comment=comment)))
            except IndexError as e:
                exception_text = f"Строка {lines.index(i) + 2} не добавилась в [res]"
                print(exception_text)
                print(e)
                res.append(ParsedData(exception_text, None))
            except Exception as e:
                exception_text = f"Неизвестная ошибка в Location.parse():\n{e}"
                print(exception_text)
                res.append(ParsedData(exception_text, None))

        return res

    def __str__(self):
        return f'Location(location_type={self.get_location_type()}, num_of_class={self.get_location_desc()}, ' \
               f'link={self.get_link()}, comment={self.get_comment()})'

    def __dict__(self):
        return {'location_type': self.get_location_type(),
                'object_id': self.get_main_id(),
                'location_desc': self.get_location_desc(),
                'profile': self.get_profile(),
                'num_of_class': self.get_num_of_class(),
                'equipment': self.get_equipment(),
                'link': self.get_link(),
                'comment': self.get_comment()}
