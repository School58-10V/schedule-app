from typing import Optional


class TeachersOnLessonRows:
    """
        Класс учителя в LessonRow. Используется для m2m отношения между
        Teacher и LessonRow
    """

    def __init__(self, teacher_id: int, lesson_row_id: int, teacher_on_lesson_row_id: Optional[int] = None):
        self.__teacher_id = teacher_id
        self.__lesson_row_id = lesson_row_id
        self.__teacher_on_lesson_row_id = teacher_on_lesson_row_id

    def get_teacher_id(self) -> int:
        return self.__teacher_id

    def get_lesson_row_id(self) -> int:
        return self.__lesson_row_id

    def get_teacher_on_lesson_row_id(self) -> Optional[int]:
        return self.__teacher_on_lesson_row_id
