
class StudentInGroup:
    """
        Класс ученика в группе. Используется для m2m отношения между
        Group и Student
    """

    def __init__(self, student_id: int, group_id: int, student_group_id: int = None):
        self.__student_id = student_id
        self.__group_id = group_id
        self.__student_group_id = student_group_id

    def get_student_id(self):
        return self.__student_id

    def get_group_id(self):
        return self.__group_id

    def get_student_group_id(self):
        return self.__student_group_id

#  Илья
