from data_model.subject_lesson import Subject
from data_model.teachers_on_lesson_rows import TeachersOnLessonRows
from data_model.timetable import TimeTable

#teacher1 = TeachersOnLessonRows.get_by_id(5, '../db')
#teachers = TeachersOnLessonRows.get_all('../db')
#print(teacher1)
#print(teachers)
#print()
#print()

#subject1 = Subject.get_by_id(5, '../db')
#subjects = Subject.get_all('../db')
#print(subject1)
#print(subjects)
#print()
#print()

print(TimeTable.get_all("../db"))
print(TimeTable.get_by_id(1897, "../db"))

