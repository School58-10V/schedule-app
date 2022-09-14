import random
from typing import Optional, List

from data_model.group import Group
from data_model.lesson_row import LessonRow
from data_model.student import Student
from data_model.students_for_groups import StudentsForGroups
from data_model.teacher import Teacher
from services.db_source_factory import DBFactory


class TeamGedzaTestClass:
    student_list = ['Хромов Михаил Романович', 'Снигур Юрий Петрович', 'Суслова Екатерина Батьковна']

    def __init__(self):
        self._db_source = DBFactory().get_db_source()
        self.student_group: Optional[Group] = None

    def run(self):
        lesson_day_list = [3, 2, 4]

        print('Создаю пустую Group')
        self.create_student_group()
        print('Заполняю ее')
        self.fill_group()
        print('Думаю какие пары им выдать')
        random_lessonrows_to_copy = self.get_random_lessons(lesson_day_list)
        print('Выдаю им пары')
        self.clone_lessons_for_random_days(random_lessonrows_to_copy, lesson_day_list)
        print('Готово! Проверяй!')
        # self.check_new_lessonrows_for_group()

    def create_student_group(self):
        teacher_name = random.choice(['Афанасьев Александр Николаевич', 'Капустин Андрей Андреевич'])
        teacher_list = Teacher.get_by_name(teacher_name, self._db_source)
        try:
            teacher_id = teacher_list[0].get_main_id()
        except IndexError:
            raise ValueError(f'Ошибка! нет учителя с именем {teacher_name}')

        self.student_group = Group(self._db_source, teacher_id)
        self.student_group.save()
        return True

    def fill_group(self):
        if self.student_group is None:
            raise Exception('Группа студентов еще не была создана! Вызовите TeamGedzaTestClass.create_student_group()')
        student_object_list = [Student.get_by_name(name, self._db_source)[0] for name in
                               TeamGedzaTestClass.student_list]
        for student in student_object_list:
            sfg = StudentsForGroups(self._db_source, student.get_main_id(), self.student_group.get_main_id())
            sfg.save()

    def get_random_lessons(self, lesson_day_list=None):
        """

        :param lesson_day_list: список, сколько пар должно быть в какой день
        """
        if lesson_day_list is None:
            lesson_day_list = [3, 3, 3]

        all_lessons = LessonRow.get_all(self._db_source)
        random_lessonrows_to_copy = list()

        while len(random_lessonrows_to_copy) < sum(lesson_day_list):
            random_lesson = random.choice(all_lessons)
            if random_lesson not in random_lessonrows_to_copy:
                random_lessonrows_to_copy.append(random_lesson)

        return random_lessonrows_to_copy

    @classmethod
    def get_random_day_numbers(cls):
        numbers = list(range(7))
        random_day_numbers = []

        while len(random_day_numbers) < 3:
            random_number = random.choice(numbers)
            if random_number not in random_day_numbers:
                random_day_numbers.append(random_number)
        return random_day_numbers

    def clone_lessons_for_random_days(self, random_lessonrows_to_copy: List[LessonRow], lesson_day_list):
        random_day_numbers = self.get_random_day_numbers()

        for i in lesson_day_list:
            # i - число пар в какой-то день
            day_of_the_week = random_day_numbers.pop()
            counter = 0
            while counter < i:
                counter += 1
                lr = random_lessonrows_to_copy.pop()
                new_lesson_row = LessonRow(
                    self._db_source, day_of_the_week, self.student_group.get_main_id(),
                    lr.get_subject_id(), lr.get_room_id(), lr.get_start_time(),
                    lr.get_end_time(), lr.get_timetable_id()
                )
                new_lesson_row.save()
                for teacher in lr.get_teachers():
                    new_lesson_row.append_teacher(teacher)


obj = TeamGedzaTestClass()
obj.run()
