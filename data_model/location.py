##               ID - Идентификационный номер места проведения урока
##     num_of_class - номер класса, в котором проходит занятие
##          Profile - профиль класса(например "хим.", если кабинет оборудован для уроков химии)
##        Equipment - оборудование в классе
##             Link - на случай дистанта ссылка(в Сибирь) для подключения к месту проведения урока
## type_of_location - Тип локации- класс, поточная аудитория, видеоконференция и т.д.
import json


class Location:
    def __init__(self, type_of_location: str, location_id: int = None, num_of_class: int = None, profile: str = None,
                 equipment: list = None, link: str = "Offline"):
        self.__location_id = location_id
        self.__num_of_class = num_of_class
        self.__profile = profile
        self.__equipment = equipment
        self.__link = link
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

    def __serialize_to_json(self):
        return json.dumps({"location_id": self.__location_id,
                       "num_of_class": self.__num_of_class,
                       "profile": self.__profile,
                       "equipment": self.__equipment,
                       "link": self.__link,
                       "type_of_location": self.__type_of_location}, ensure_ascii=False)

    def save(self):
        with open("./db/locations.json", mode="w", encoding='utf-8') as data_file:
            data_file.write(self.__serialize_to_json())
