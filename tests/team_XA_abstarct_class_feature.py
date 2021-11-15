from data_model.subject_lesson import Subject
from data_model.teachers_on_lesson_rows import TeachersOnLessonRows
from data_model.group import Group
# from data_model.timetable import TimeTable
#
teacher = TeachersOnLessonRows(2, 3, teacher_on_lesson_row_id=5)
teacher.save('../db')
teacher1 = TeachersOnLessonRows.get_by_id(5, '../db')
teachers = TeachersOnLessonRows.get_all('../db')
print(teacher1)
print(teachers)
teacher1.delete('../db')
teachers = TeachersOnLessonRows.get_all('../db')
print(teachers)
print(teacher1)
print()
print()

subject = Subject(subject_id=5)
subject.save('../db')
subject1 = Subject.get_by_id(5, '../db')
subjects = Subject.get_all('../db')
print(subject1)
print(subjects)
subject1.delete('../db')
subjects = Subject.get_all('../db')
print(subjects)
print()

group1 = Group(1, '', 1, 'k', 10)
group1.save('../db')
group2 = Group.get_by_id(10, '../db')
groups = Group.get_all('../db')
print(group2)
print(groups)
group2.delete('../db')
groups = Group.get_all('../db')
print(groups)
print(group2)

# print(TimeTable.get_all("../db"))
# print(TimeTable.get_by_id(1898, "../db"))
#
