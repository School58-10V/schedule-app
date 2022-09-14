from data_model.student import Student
from data_model.subject import Subject
from data_model.teacher import Teacher
from data_model.teachers_for_subjects import TeachersForSubjects
from data_model.lesson_row import LessonRow

from schedule_app import app
import datetime
import random


class TestGenerator:
    def __init__(self):
        self.creators = [{
                'full_name': 'Бугаенко Оля Алексеевна',
                'date_of_birth': 'какой-то текст'
            },
            {
                'full_name': 'Вовк Михаил',
                'date_of_birth': datetime.date(2004, 11, 17)
            },
            # Ваня будет потом использован для демонстрации
            # {
            #     'full_name': 'Шаталов Иван',
            # }
        ]

        creators_to_add = self.check_creators()
        self.add_creators(creators_to_add)

    def check_creators(self):
        no_record = []

        for creator in self.creators:
            student = Student.get_by_name(creator['full_name'], app.config.get('schedule_db_source'))

            if len(student) == 0:
                no_record.append(creator)

        return no_record

    @staticmethod
    def add_creators(creators):
        for creator in creators:
            new_student = Student(**creator, db_source=app.config.get('schedule_db_source')).save()

    @staticmethod
    def choose_subjects(amount) -> list:
        subjects = Subject.get_all(db_source=app.config.get('schedule_db_source'))

        subjects_today = random.sample(subjects, amount)
        return subjects_today

    @staticmethod
    def add_teacher(teacher):
        new_teacher = Teacher(**teacher, db_source=app.config.get('schedule_db_source')).save()
        return new_teacher

    def get_subject_teacher_pairs(self, amount):
        subjects = self.choose_subjects(amount)
        teachers = []

        for sub in subjects:
            all_teachers = TeachersForSubjects.get_teachers_by_subject_id(sub.get_main_id(),
                                                                          db_source=app.config.get(
                                                                              'schedule_db_source'))

            if len(all_teachers) != 0:
                teachers.append(random.choice(all_teachers))
            else:
                print("Нужен новый учитель:")
                fio = input("ИФО:")
                bio = input("информация об учителе:")
                contacts = input("контакты учителя:")
                office_id = input("закреплённый кабинет:")
                teachers.append(self.add_teacher({fio: "Новый Учитель", office_id: office_id,
                                                  bio: bio, contacts: contacts}))

        return subjects, teachers

    def create_schedule(self, amount_of_lessons) -> None:
        for day_of_week in amount_of_lessons.keys():
            amount = amount_of_lessons[day_of_week]
            subjects, teachers = self.get_subject_teacher_pairs(amount)

            start_time='900'
            #TODO: дописать добавление в lesson row


def print_all_students():
    students = Student.get_all(app.config.get('schedule_db_source'))

    for el in students:
        print(el.get_full_name())


if __name__ == '__main__':
    gen = TestGenerator()

    # print_all_students()
    lessons = {
        0: 2,
        1: 3,
        2: 2
    }

    gen.create_schedule(lessons)