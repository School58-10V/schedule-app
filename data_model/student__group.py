class Student__Group:
    # TODO: разве здесь правильно использовать нижние подчеркивания? но и камел касе тоже такое себе
    """
        Класс ученика в группе. Используется для m2m отношения между
        Group и Student
    """

    def __init__(self, student_id: int, group_id: int):
        self.__student_id = student_id
        self.__group_id = group_id

    def get_student_id(self):
        return self.__student_id

    def get_group_id(self):
        return self.__group_id
