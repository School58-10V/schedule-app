from typing import Optional


class Group:
    """
        Класс группы.
    """
    def __init__(
            self, teacher_id: int, class_letter: str, grade: int,
            profile_name: str, group_id: Optional[int] = None
    ):
        self.__teacher_id = teacher_id
        self.__class_letter = class_letter
        self.__grade = grade
        self.__profile_name = profile_name  # should be empty if no profile exists
        self.__group_id = group_id

    def get_teacher_id(self) -> int:
        return self.__teacher_id

    def get_letter(self) -> str:
        return self.__class_letter

    def get_grade(self) -> int:
        return self.__grade

    def get_profile_name(self) -> str:
        return self.__profile_name

    def get_id(self) -> Optional[int]:
        return self.__group_id
