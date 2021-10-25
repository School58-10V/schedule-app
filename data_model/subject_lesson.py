from random import randrange


class Subject:
    def __init__(self, name, subjectid=None):
        self.__subject_name = name
        self.__subject_id = subjectid

    @property
    def subject_id(self):
        return self.__subject_id

    @property
    def subject_name(self):
        return self.__subject_name
