class Subject:
    def __init__(self, name: str, subject_id: int = None):
        self.__subject_name = name
        self.__subject_id = subject_id

    def get_subject_id(self) -> int:
        return self.__subject_id

    def get_subject_name(self) -> str:
        return self.__subject_name
