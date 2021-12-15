from __future__ import annotations  # нужно чтобы parse мог быть типизирован
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
        self._object_id = object_id
        self.__location_desc = location_desc
        self.__profile = profile
        self.__num_of_class = num_of_class
        self.__equipment = equipment
        self.__link = link
        self.__location_type = location_type
        self.__comment = comment

    def get_location_desc(self):
        return self.__location_desc

    def get_profile(self):
        return self.__profile

    def get_equipment(self):
        return self.__equipment

    def get_link(self):
        return self.__link

    def get_location_type(self):
        return self.__location_type

    def get_comment(self):
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
                res.append(ParsedData(None, Location(db_source=db_source,
                                                     location_type=location_type, link=link,
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
        return f'Location(location_type={self.__location_type}, num_of_class={self.__location_desc}, ' \
               f'link={self.__link}, comment={self.__comment})'

    def __dict__(self):
        return {'object_id': self._object_id,
                'location_desc': self.__location_desc,
                'profile': self.__profile,
                'num_of_class': self.__num_of_class,
                'equipment': self.__equipment,
                'link': self.__link,
                'location_type': self.__location_type,
                'comment': self.__comment}

