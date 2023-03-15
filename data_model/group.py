from __future__ import annotations  # нужно чтобы parse мог быть типизирован

from data_model.abstract_model import AbstractModel
from typing import Optional, List, TYPE_CHECKING

from data_model.lesson_row import LessonRow
from data_model.students_for_groups import StudentsForGroups
from data_model.parsed_data import ParsedData
from data_model.student import Student

if TYPE_CHECKING:
    from adapters.db_source import DBSource


class Group(AbstractModel):
    """
        Класс группы.
    """
    def __init__(
            self, db_source: DBSource, teacher_id: int, class_letter: Optional[str] = None, grade: Optional[int] = None,
            profile_name: Optional[str] = None, object_id: Optional[int] = None
    ):
        super().__init__(db_source)
        self.__teacher_id = teacher_id
        self.__class_letter = class_letter
        self.__grade = grade
        self.__profile_name = profile_name  # should be empty if no profile exists
        self._object_id = object_id

    def get_teacher_id(self) -> int:
        return self.__teacher_id

    def get_letter(self) -> str:
        return self.__class_letter

    def get_grade(self) -> int:
        return self.__grade

    def get_profile_name(self) -> str:
        return self.__profile_name

    @staticmethod
    def parse(file_location: str, db_source: DBSource) -> List[(Optional[str], Optional[Group])]:
        # ввод; адрес файла,
        with open(file_location, encoding='utf-8') as file:
            # файл теперь в file
            lines = file.read().split('\n')[1:]
            lines = [i.split(';') for i in lines]
            # превращаем файл в лист
            res = []
            for i in lines:
                # тут трай
                try:
                    teacher_id = i[0]
                    class_letter = i[1]
                    grade = i[2]
                    profile_name = i[3]
                    # тут наполняем список
                    res.append(ParsedData(None, Group(db_source=db_source,
                                                      teacher_id=int(teacher_id),
                                                      class_letter=class_letter,
                                                      grade=int(grade),
                                                      profile_name=profile_name)))

                except IndexError as e:
                    exception_text = f"Строка {lines.index(i) + 2} не добавилась в [res]"
                    print(exception_text)
                    print(e)
                    res.append(ParsedData(exception_text, None))
                except Exception as e:
                    exception_text = f"Неизвестная ошибка в Group.parse():\n{e}"
                    print(exception_text)
                    res.append(ParsedData(exception_text, None))
        # тут ретёрнем список
        return res

    def __str__(self) -> str:
        return f'Group(teacher_id={self.get_teacher_id()}, class_letter={self.get_letter()}, ' \
               f'grade={self.get_grade()}, profile_name={self.get_profile_name()}, object_id={self.get_main_id()})'

    def __dict__(self) -> dict:
        return {"teacher_id": self.get_teacher_id(),
                "class_letter": self.get_letter(),
                "grade": self.get_grade(),
                "profile_name": self.get_profile_name(),
                "object_id": self.get_main_id()}

    def get_all_students(self) -> List[Student]:
        """
           Возвращает список объектов GroupsForStudents используя db_source данный в __init__()
           :return: список словарей объектов Student
        """
        return StudentsForGroups.get_student_by_group_id(self.get_main_id(), self._db_source)

    def append_student(self, student: Student) -> Group:
        """
            Сохраняем нового студента для группы. На ввод объект класса Student, который мы хотим
            добавить, на вывод self
        """
        for i in StudentsForGroups.get_student_by_group_id(self.get_main_id(), self.get_db_source()):
            if i.get_main_id() == student.get_main_id():
                return self

        StudentsForGroups(self._db_source, student_id=student.get_main_id(), group_id=self.get_main_id()).save()
        return self

    def get_lesson_rows(self) -> List[LessonRow]:
        return LessonRow.get_lesson_rows_by_group_id(self.get_main_id(), self.get_db_source())

    def remove_student(self, student: Student) -> Group:
        """
            Удалять студента для группы. На ввод объект класса Student, который мы хотим
            удалить, на вывод self
        """
        # Берем все объекты смежной сущности, проходим по нему циклом
        for i in StudentsForGroups.get_by_student_and_group_id(db_source=self._db_source, group_id=self.get_main_id(),
                                                               student_id=student.get_main_id()):

            # И все удаляем
            i.delete()
        return self

    @classmethod
    def get_by_class_letters(cls, db_source: DBSource, class_letter: str, grade: int) -> List[Group]:

        list_of_groups = db_source.get_by_query(cls._get_collection_name(),
                                                {'class_letter': class_letter, 'grade': grade})
        return [Group(**i, db_source=db_source) for i in list_of_groups]
