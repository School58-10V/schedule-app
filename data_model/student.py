class Student:
    def __init__(self, student_id: int, full_name: str, class_id: int):
        self.__id = student_id
        self.__full_name = full_name
        self.__class_id = class_id
        # self.__phone_number = phone_number
        # self.__parents_phone_number = parents_phone_number

    def get_id(self):
        return self.__id

    def get_full_name(self):
        return self.__full_name

    def get_class_id(self):
        return self.__class_id

