from __future__ import annotations  # нужно чтобы parse мог быть типизирован

from schedule_app import app

from data_model.abstract_model import AbstractModel
from typing import List, Optional, TYPE_CHECKING
from data_model.student import Student
from data_model.teacher import Teacher
from data_model.students_for_groups import StudentsForGroups
from data_model.teachers_for_lesson_rows import TeachersForLessonRows
import hashlib

if TYPE_CHECKING:
    from adapters.db_source import DBSource


class User(AbstractModel):
    # status codes
    STUDENT = 1
    TEACHER = 2
    ADMINISTRATOR = 3
    OTHER = 4

    def __init__(self, db_source: DBSource, name: str, login: str, hash_password: Optional[str] = None,
                 password: Optional[str] = None, status: int = 1, ref_id: int = -1, object_id: int = None):
        """
            :param db_source: ссылка на бд
            :param login: логин
            :param password_hash: пароль
            :param name: имя пользователя
            :param status: статус пользователя: 1 - ученик, 2 - учитель, 3 - администрация, 4 - прочие
        """
        super().__init__(db_source)
        self.__login = login
        if hash_password is None and password is not None:
            self.__password_hash = hashlib.sha256(password.encode()).hexdigest()
        elif password is None and hash_password is not None:
            self.__password_hash = hash_password
        else:
            raise ValueError('Ошибка создания: должен присутствовать password ИЛИ hash_password')
        self.__name = name
        self.__ref_id = ref_id
        self.__object_id = object_id
        self.__status = status

        self.find_reference(status)

    @classmethod
    def get_by_login(cls, login: str, db_source: DBSource) -> Optional[User]:
        data = db_source.get_by_query(collection_name=cls._get_collection_name(), query={'login': login})
        if len(data) == 0:
            raise ValueError('No such user')
        if len(data) > 1:
            raise ValueError('User login is duplicated')
        return User(**data[0], db_source=db_source)

    def get_login(self) -> str:
        return self.__login

    def get_password_hash(self) -> str:
        return self.__password_hash

    def get_name(self) -> str:
        return self.__name

    def get_status(self) -> int:
        return self.__status

    def get_ref_id(self) -> int:
        return self.__ref_id

    def get_main_id(self) -> int:
        return self.__object_id

    def set_ref_id(self, ref_id):
        self.__ref_id = ref_id

    def __str__(self):
        return f"Пользователь {self.get_name()} с логином {self.get_login()}"

    def __dict__(self) -> dict:
        return {"name": self.get_name(),
                "login": self.get_login(),
                "hash_password": self.get_password_hash(),
                'status': self.get_status(),
                'object_id': self.get_main_id()}

    def get_profile_information(self):
        information = {
            'name': self.get_name(),
            'id': self.get_ref_id(),
            'role': self.get_status()
        }

        if self.get_ref_id() == -1:
            try:
                self.find_reference(self.get_status())
            except ValueError:
                return information

        if self.get_status() == User.STUDENT:
            information['groups_id'] = StudentsForGroups.get_groups_ids_for_student(
                                            information['id'], db_source=app.config.get('schedule_db_source'))
        if self.get_status() == User.TEACHER:
            TeachersForLessonRows.get_lesson_rows_ids_by_teacher_id(
                information['id'], db_source=app.config.get('schedule_db_source'))

        return information

    def compare_hash(self, password: str) -> bool:
        return self.__password_hash == hashlib.sha256(password.encode()).hexdigest()

    def find_reference(self, table: int = None):
        if table is None:
            connected_students = Student.get_by_name(self.get_name(), db_source=app.config.get('schedule_db_source'))
            connected_teachers = Teacher.get_by_name(self.get_name(), db_source=app.config.get('schedule_db_source'))

            if len(connected_students) + len(connected_teachers) > 1:
                raise ValueError('Name is duplicated')
            if len(connected_students) + len(connected_teachers) == 0:
                raise ValueError('No such student and teacher')

            if len(connected_students) == 1:
                self.set_ref_id(connected_students[0].get_main_id())
            else:
                self.set_ref_id(connected_teachers[0].get_main_id())
        if table == User.STUDENT:
            connected_students = Student.get_by_name(self.get_name(), db_source=app.config.get('schedule_db_source'))

            if len(connected_students) > 1:
                raise ValueError('Name is duplicated')
            if len(connected_students) == 0:
                raise ValueError('No such student')

            if len(connected_students) == 1:
                self.set_ref_id(connected_students[0].get_main_id())
        if table == User.TEACHER:
            connected_teachers = Teacher.get_by_name(self.get_name(), db_source=app.config.get('schedule_db_source'))

            if len(connected_teachers) > 1:
                raise ValueError('Name is duplicated')
            if len(connected_teachers) == 0:
                raise ValueError('No such teacher')

            if len(connected_teachers) == 1:
                self.set_ref_id(connected_teachers[0].get_main_id())


