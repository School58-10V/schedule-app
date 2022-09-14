import random
from typing import Optional, List

from data_model.group import Group
from data_model.lesson_row import LessonRow
from data_model.location import Location
from data_model.student import Student
from data_model.students_for_groups import StudentsForGroups
from data_model.subject import Subject
from data_model.teacher import Teacher
from services.db_source_factory import DBFactory


class TeamGedzaTestClass:
    """
        Класс для теста работы с БД и модельками.

        Есть возможность создавать группу учеников, наполнять ее,
         выдавать ей рандомные уроки, смотреть инфу по группе.
    """

    # Сколько пар в какие дни должны быть
    # Здесь написано, что должно быть три дня по три пары
    DEFAULT_LESSON_DAY_LIST_DISTRIBUTION = [3, 3, 3]

    def __init__(self, student_list):
        self.student_list = student_list
        self._db_source = DBFactory().get_db_source()
        self._student_group: Optional[Group] = None

    def run(self, lesson_day_list: Optional[List[int]] = None):
        if lesson_day_list is None:
            lesson_day_list = TeamGedzaTestClass.DEFAULT_LESSON_DAY_LIST_DISTRIBUTION

        print('Создаю пустую Group')
        self.create_student_group()
        print('Заполняю ее')
        self.fill_group()
        print('Думаю какие пары им выдать')
        random_lessonrows_to_copy = self.get_random_lessons(lesson_day_list)
        print('Выдаю им пары')
        self.clone_lessons_for_random_days(random_lessonrows_to_copy, lesson_day_list)
        # self._student_group = Group.get_by_id(64, self._db_source)
        print('Готово, запрашиваю БД по поводу данных которые мы только что создали!')
        self.check_new_lessonrows_for_group()

    def create_student_group(self):
        teacher_name = random.choice(['Афанасьев Александр Николаевич', 'Капустин Андрей Андреевич'])
        teacher_list = Teacher.get_by_name(teacher_name, self._db_source)
        try:
            teacher_id = teacher_list[0].get_main_id()
        except IndexError:
            raise Exception(f'Ошибка! нет учителя с именем {teacher_name}')

        self._student_group = Group(self._db_source, teacher_id)
        self._student_group.save()
        return True

    def fill_group(self):
        if self._student_group is None:
            raise Exception('Группа студентов еще не была создана! Вызовите TeamGedzaTestClass.create_student_group()')
        student_object_list = [
            Student.get_by_name(name, self._db_source)[0]
            for name in
            self.student_list
        ]
        for student in student_object_list:
            sfg = StudentsForGroups(self._db_source, student.get_main_id(), self._student_group.get_main_id())
            sfg.save()

    def get_random_lessons(self, lesson_day_list=None):
        """

        :param lesson_day_list: список, сколько пар должно быть в какой день
        """

        all_lessons = LessonRow.get_all(self._db_source)
        random_lessonrows_to_copy = list()

        while len(random_lessonrows_to_copy) < sum(lesson_day_list):
            random_lesson = random.choice(all_lessons)
            if random_lesson not in random_lessonrows_to_copy:
                random_lessonrows_to_copy.append(random_lesson)

        return random_lessonrows_to_copy

    @classmethod
    def get_random_day_numbers(cls, lesson_day_list: List[int]):
        numbers = list(range(7))
        random_day_numbers = []

        while len(random_day_numbers) < len(lesson_day_list):
            random_number = random.choice(numbers)
            if random_number not in random_day_numbers:
                random_day_numbers.append(random_number)
        return random_day_numbers

    def clone_lessons_for_random_days(self, random_lessonrows_to_copy: List[LessonRow], lesson_day_list: List[int]):
        random_day_numbers = self.get_random_day_numbers(lesson_day_list)

        for i in lesson_day_list:
            # i - число пар в какой-то день
            day_of_the_week = random_day_numbers.pop()
            counter = 0
            while counter < i:
                counter += 1
                lr = random_lessonrows_to_copy.pop()
                new_lesson_row = LessonRow(
                    self._db_source, day_of_the_week, self._student_group.get_main_id(),
                    lr.get_subject_id(), lr.get_room_id(), lr.get_start_time(),
                    lr.get_end_time(), lr.get_timetable_id()
                )
                new_lesson_row.save()
                for teacher in lr.get_teachers():
                    new_lesson_row.append_teacher(teacher)

    def check_new_lessonrows_for_group(self):
        """
        Делает много принтов по тем данным которые мы только что добавили.

        :return: None
        """

        student_list = StudentsForGroups.get_student_by_group_id(self._student_group.get_main_id(), self._db_source)
        student_name_string = ", ".join([i.get_full_name() for i in student_list])
        teacher_name = Teacher.get_by_id(self._student_group.get_teacher_id(), self._db_source).get_fio()
        print(f'Информация для группы с ИД {self._student_group.get_main_id()}, ее ученики: {student_name_string}, '
              f'ее учитель: {teacher_name}')
        print()
        print(f'Список их уроков: ')
        lr_counter = 1
        last_day_of_the_week = None
        for lr in LessonRow.get_lesson_rows_by_group_id(self._student_group.get_main_id(), self._db_source):
            day_of_the_week_dict = {0: 'Понедельник', 1: 'Вторник', 2: 'Среду',
                                    3: 'Четверг', 4: 'Пятницу', 5: 'Субботу', 6: 'Воскресенье'}
            cabinet_number = Location.get_by_id(lr.get_room_id(), self._db_source).get_num_of_class()
            teacher_list_string = ", ".join([t.get_fio() for t in lr.get_teachers()])
            subject_name = Subject.get_by_id(lr.get_subject_id(), self._db_source).get_subject_name()
            print(f'{lr_counter}. Урок {subject_name} в {day_of_the_week_dict[lr.get_day_of_the_week()]}, с '
                  f'{lr.prettify_time(lr.get_start_time())} до {lr.prettify_time(lr.get_end_time())}, '
                  f'в кабинете #{cabinet_number} '
                  f'у учителя(ей) {teacher_list_string}.')
            lr_counter += 1

            # Делаем print() если переходим на следующий день недели
            if (last_day_of_the_week is not None) and\
                    last_day_of_the_week != day_of_the_week_dict[lr.get_day_of_the_week()]:
                print()
            last_day_of_the_week = day_of_the_week_dict[lr.get_day_of_the_week()]


student_list = ['Хромов Михаил Романович', 'Снигур Юрий Петрович', 'Суслова Екатерина Батьковна']
obj = TeamGedzaTestClass(student_list)
obj.run()
