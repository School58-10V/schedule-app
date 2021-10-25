class SchoolClass:
    """
        Класс класса (хах).
    """
    def __init__(
            self, school_class_id: int, teacher_id: int, class_letter: str, grade: int,
            profile_name: str
    ):
        # TODO: добавить описания каждой из переменных
        self.__id = school_class_id
        self.__teacher_id = teacher_id
        self.__class_letter = class_letter
        self.__grade = grade
        self.__profile_name = profile_name  # should be empty if no profile exists

    def get_id(self):
        return self.__id

    def get_teacher_id(self):
        # TODO: если учителей у одной группы по предмету несколько, то это сломается.
        return self.__teacher_id

    def get_letter(self):
        return self.__class_letter

    def get_grade(self):
        return self.__grade

    def get_profile_name(self):
        return self.__profile_name
