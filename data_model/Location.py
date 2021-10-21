##               ID - Идентификационный номер места проведения урока
##     num_of_class - номер класса, в котором проходит занятие
##          Profile - профиль класса(например "хим.", если кабинет оборудован для уроков химии)
##        Equipment - оборудование в классе
##             Link - на случай дистанта ссылка(в Сибирь) для подключения к месту проведения урока
## type_of_location - Тип локации- класс, поточная аудитория, видеоконференция и т.д.


class Location_Of_Lessons:
    def __init__(self, ID, num_of_class=-1, profile="Everything", equipment=["Standart"], link="Offline",
                 type_of_location="Class"):
        self.__ID = ID
        self.__num_of_class = num_of_class
        self.__profile = profile
        self.__equipment = equipment
        self.__link = link
        self.__type_of_location = type_of_location
