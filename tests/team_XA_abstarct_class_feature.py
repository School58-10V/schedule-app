from datetime import date

from data_model.subject_lesson import Subject
from data_model.teachers_on_lesson_rows import TeachersOnLessonRows
from data_model.group import Group
from data_model.timetable import TimeTable
from data_model.no_learning_period import NoLearningPeriod

teacher = TeachersOnLessonRows(2, 3, object_id=5)
teacher.save('../db')
teacher1 = TeachersOnLessonRows(4, 6, object_id=5)
teachers = TeachersOnLessonRows.get_all('../db')
print(teacher1)
print(teachers)
teacher1.delete('../db')
teachers = TeachersOnLessonRows.get_all('../db')
print(teachers)
print(teacher1)
print()
print()

subject = Subject(object_id=5)
subject.save('../db')
subject1 = Subject(subject_name='Art', object_id=5)
subjects = Subject.get_all('../db')
print(subject1)
print(subjects)
subject1.delete('../db')
subjects = Subject.get_all('../db')
print(subjects)
print(subject1.get_main_id(), 'id subject')
print()
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
print()
print()

table = TimeTable(2000, object_id=36)
table.save("../db")
print(TimeTable.get_all("../db"))
print(TimeTable.get_by_id(36, "../db"))
table.delete("../db")
print(table)
print()

print(NoLearningPeriod.get_all("../db"))
period = NoLearningPeriod(2021, 2022, object_id=15)
period.save("../db")
print(NoLearningPeriod.get_by_id(15, "../db"))
print(NoLearningPeriod.get_all("../db"))
period.delete("../db")
print(NoLearningPeriod.get_all("../db"))
