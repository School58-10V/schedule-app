from data_model.student import Student
from data_model.subject import Subject
from data_model.teacher import Teacher
from data_model.teachers_for_subjects import TeachersForSubjects
from data_model.lesson_row import LessonRow
from data_model.location import Location
from data_model.group import Group
from data_model.students_for_groups import StudentsForGroups

from schedule_app import app
import datetime
import random

timetable = [(900, 1040), (1100, 1240), (1300, 1440), (1500, 1640)]
GROUP_ID = 72


class TestGenerator:
    def __init__(self):
        self.creators_info = [{
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

        added, creators_to_add = self.check_creators()

        self.creators = self.add_creators(creators_to_add)
        self.creators += added

        # self.group = self.create_group(grade=11, name='Vareniki', profile_name='Гении')
        self.group = Group.get_by_id(element_id=GROUP_ID, db_source=app.config.get('schedule_db_source'))

    def check_creators(self):
        no_record = []
        added = []

        for creator in self.creators_info:
            student = Student.get_by_name(creator['full_name'], app.config.get('schedule_db_source'))

            if len(student) == 0:
                no_record.append(creator)
            else:
                added.append(student[0])

        return added, no_record

    @staticmethod
    def add_creators(creators):
        added = []
        for creator in creators:
            new_student = Student(**creator, db_source=app.config.get('schedule_db_source')).save()
            added.append(new_student)

        return added

    def create_group(self, grade, name, profile_name, students, teacher_id=4):
        new_group = Group(teacher_id=teacher_id, grade=grade, class_letter=name, profile_name=profile_name,
                          db_source=app.config.get('schedule_db_source')).save()

        self.link_students_to_groups(students, new_group)
        return new_group

    @staticmethod
    def link_students_to_groups(students, group):
        for stud in students:
            new_link = StudentsForGroups(student_id=stud.get_main_id(), group_id=group.get_main_id(),
                                         db_source=app.config.get('schedule_db_source')).save()

    @staticmethod
    def choose_subjects(amount) -> list:
        subjects = Subject.get_all(db_source=app.config.get('schedule_db_source'))

        subjects_today = random.sample(subjects, amount)
        return subjects_today

    @staticmethod
    def create_office(number):
        new_office = Location(location_type='classroom', num_of_class=number,
                              db_source=app.config.get('schedule_db_source')).save()

        return new_office

    @staticmethod
    def create_teacher(teacher):
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
                print("Создание нового учителя...")
                new_office = self.create_office(random.randint(160, 420))

                information = {
                    'fio': 'Новый Учитель',
                    'bio': 'bio...',
                    'contacts': 'contacts...',
                    'office_id': new_office.get_main_id()
                }

                new_teacher = self.create_teacher(information)
                print(f'Создан учитель с id: {new_teacher.get_main_id()}')

                TeachersForSubjects(teacher_id=new_teacher.get_main_id(), subject_id=sub.get_main_id(),
                                    db_source=app.config.get('schedule_db_source')).save()

                teachers.append(new_teacher)

        return subjects, teachers

    def create_schedule(self, amount_of_lessons) -> None:
        for day_of_week in amount_of_lessons.keys():
            amount = amount_of_lessons[day_of_week]
            subjects, teachers = self.get_subject_teacher_pairs(amount)

            for i, (subject, teacher) in enumerate(zip(subjects, teachers)):
                new_lessonrow = LessonRow(day_of_the_week=day_of_week, group_id=self.group.get_main_id(),
                                          start_time=timetable[i][0], end_time=timetable[i][1],
                                          subject_id=subject.get_main_id(), room_id=teacher.get_office_id(),
                                          timetable_id=1, db_source=app.config.get('schedule_db_source')).save()

                print(new_lessonrow.get_main_id())


def print_all_students():
    students = Student.get_all(app.config.get('schedule_db_source'))

    for el in students:
        print(el.get_full_name())


if __name__ == '__main__':
    gen = TestGenerator()

    # for el in gen.creators:
    #     print(el.get_main_id())
    #
    # print(gen.group.get_main_id())

    lessons = {
        0: 2,
        1: 3,
        2: 2
    }

    gen.create_schedule(lessons)
