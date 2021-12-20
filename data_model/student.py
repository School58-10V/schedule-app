from __future__ import annotations  # нужно чтобы parse мог быть типизирован
from datetime import datetime
from data_model.parsed_data import ParsedData
from typing import Optional, List, TYPE_CHECKING

from data_model.abstract_model import AbstractModel
from data_model.students_for_groups import StudentsForGroups


if TYPE_CHECKING:
    from adapters.file_source import FileSource
    from data_model.group import Group


class Student(AbstractModel):
    """
        Класс ученика.
        full name - полное имя студента
        date_of_birth - дата рождения ученика
        object_id - id студента
        contacts - контакты родителей ученика
        bio - биография студента
    """

    def __init__(
            self, db_source: FileSource, full_name: str, date_of_birth: datetime.date, object_id: Optional[int] = None,
            contacts: Optional[str] = None, bio: Optional[str] = None
            ):
        super().__init__(db_source)
        self.__full_name = full_name
        self.__date_of_birth = date_of_birth
        self._object_id = object_id
        self.__contacts = contacts
        self.__bio = bio

    def get_full_name(self) -> str:
        return self.__full_name

    def get_date_of_birth(self) -> datetime.date:
        return self.__date_of_birth

    def get_contacts(self) -> Optional[str]:
        return self.__contacts

    def get_bio(self) -> Optional[str]:
        return self.__bio

    @staticmethod
    def parse(file_location, db_source: FileSource) -> List[(Optional[str], Optional[Student])]:
        with open(file_location, encoding='utf-8') as f:
            lines = [i.split(';') for i in f.read().split('\n')[1:]]
            res = []

            for i in lines:
                try:
                    full_name = i[0]
                    date_of_birth = datetime.strptime(i[1], '%d.%m.%Y').date()
                    contacts = str(i[2])
                    bio = i[3]

                    res.append(ParsedData(None, Student(db_source, full_name=full_name, date_of_birth=date_of_birth,
                                                        contacts=contacts, bio=bio)))
                except IndexError as e:
                    exception_text = f"Строка {lines.index(i) + 1} не добавилась в [res]"
                    print(exception_text)
                    print(e)
                    res.append(ParsedData(exception_text, None))
                except Exception as e:
                    exception_text = f"Неизвестная ошибка в Student.parse():\n{e}"
                    print(exception_text)
                    res.append(ParsedData(exception_text, None))

        return res

    def __str__(self):
        return f'Student(full_name = {self.__full_name}, date_of_birth = {self.__date_of_birth}, ' \
               f'contacts = {self.__contacts}, bio =  {self.__bio}) '

    def __dict__(self) -> dict:
        return {"full_name": self.get_full_name(),
                "date_of_birth": self.get_date_of_birth(),
                "object_id": self.get_main_id(),
                "contacts": self.get_contacts(),
                "bio": self.get_bio()}
  
    def get_all_groups(self) -> List[Group]:
        """
           Ссылается на класс StudentsForGroups и использует его метод
           :return: список объектов Group
        """
        return StudentsForGroups.get_group_by_student_id(self.get_main_id(), self.get_db_source())

    def append_group(self, group: Group) -> Student:
        """
            Сохраняем новую группу для этого студента, используя класс
        :param group: объект класса Group, который мы хотим добавить этому студенту StudentsForGroups
        :return: себя
        """
        if len(self._db_source.get_by_query(StudentsForGroups.__name__, {'group_id': group.get_main_id()})) == 0:
            StudentsForGroups(self._db_source, group_id=group.get_main_id(), student_id=self.get_main_id()).save()
        return self

    def delete_group(self, group: Group) -> Student:
        """
            Удаляем новую группу для этого студента, используя класс
        :param group: объект класса Group, который мы хотим удалить этому студенту StudentsForGroups
        :return: себя
        """
        if len(self._db_source.get_by_query(StudentsForGroups.__name__, {'group_id': group.get_main_id()})) == 0:
            StudentsForGroups(self._db_source, group_id=group.get_main_id(), student_id=self.get_main_id()).delete()
        return self
