from __future__ import annotations
import json
from typing import Optional, List
##               ID - Идентификационный номер места проведения урока
##     num_of_class - номер класса, в котором проходит занятие
##          Profile - профиль класса(например "хим.", если кабинет оборудован для уроков химии)
##        Equipment - оборудование в классе
##             Link - на случай дистанта ссылка(в Сибирь) для подключения к месту проведения урока
## type_of_location - Тип локации- класс, поточная аудитория, видеоконференция и т.д.


class Location:
    def __init__(self, type_of_location: str, location_id: int = None, num_of_class: int = None, profile: str = None,
                 equipment: list = None, comment: str = None, location_desc: str = None, link: str = "Offline"):
        self.__location_id = location_id
        self.__num_of_class = num_of_class
        self.__profile = profile
        self.__equipment = equipment
        self.__link = link
        self.__comment = comment
        self.__location_desc = location_desc
        self.__type_of_location = type_of_location

    def get__location_id(self):
        return self.__location_id

    def get_num_of_class(self):
        return self.__num_of_class

    def get_profile(self):
        return self.__profile

    def get_equipment(self):
        return self.__equipment

    def get_link(self):
        return self.__link

    def get_type_of_location(self):
        return self.__type_of_location

    def __serialize_to_json(self, records: list) -> str:
        # Добавляем новый объект в список
        records.append({"location_id": self.__location_id,
                           "num_of_class": self.__num_of_class,
                           "profile": self.__profile,
                           "equipment": self.__equipment,
                           "link": self.__link,
                           "type_of_location": self.__type_of_location})
        return json.dumps(records, ensure_ascii=False, indent=4)

    @classmethod
    def read_json_db(cls, db_path) -> list:
        try:
            with open(f"{db_path}/{cls.name}.json", mode="r", encoding='utf-8') as data_file:
                record = json.loads(data_file.read())
                return record
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return []

    def save(self, output_path: str = './db'):
        current_records = self.read_json_db(output_path)
        target_json = self.serialize_to_json(current_records)
        with open(f"{output_path}/{type(self).name}.json", mode="w", encoding='utf-8') as data_file:
            data_file.write(target_json)

    def __str__(self):
        return f'Location(type_of_location={self.__type_of_location}, name={self.__location_desc}, ' \
               f'link={self.__link}, comment={self.__comment})'

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
