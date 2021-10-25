class Student:
    """
        Класс ученика.
    """
    def __init__(self, student_id: int, full_name: str, class_id: int):
        # Если student_id == -1, то он еще не установлен. Ставим None.
        if student_id == -1:
            self.__student_id = None
        else:
            self.__student_id = student_id

        self.__full_name = full_name
        self.__class_id = class_id
        # self.__phone_number = phone_number
        # self.__parents_phone_number = parents_phone_number

    def get_id(self):
        return self.__student_id

    def get_full_name(self):
        return self.__full_name

    def get_class_id(self):
        return self.__class_id

