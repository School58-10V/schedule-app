class Subject:
    def __init__(self, name: str, subjectid: int = None):
        self.__subject_name = name
        self.__subject_id = subjectid

    def get_subject_id(self):
        return self.__subject_id

    def get_subject_name(self):
        return self.__subject_name
