from data_model.subject_lesson import Subject
from data_model.timetable import TimeTable
from data_model.teachers_on_lesson_rows import TeachersOnLessonRows


subject1 = Subject('Art', 1)
subject1.save('../db')

subject2 = Subject()
subjects = subject2.parse('../data_examples/subject_test.csv')
print(subject2)
subject2.save('../db')

subject3 = subjects[0][1]
print(subject3)
subject3.save('../db')
print()
print()

timetable1 = TimeTable(2021, 1897)
timetable = timetable1.parse("../data_examples/timetable_test.csv")
print(timetable1)
print(timetable)
timetable1.save('../db')
print()
print()

teacher = TeachersOnLessonRows(1, 2)
teacher.save('../db')
teachers = teacher.parse('../data_examples/teachers_on_lesson_rows_test.csv')
print(teacher)
print(teachers)
