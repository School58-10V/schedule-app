from data_model.group import Group
from data_model.lesson_row import LessonRow
from data_model.student import Student
from data_model.subject import Subject
from data_model.teacher import Teacher
from interfaces.cli_team_b import CLI
from adapters.file_source import FileSource


fs = FileSource('../db')
subject_1 = Subject(db_source=fs, subject_name="Алгебра").save()
subject_2 = Subject(db_source=fs, subject_name="Физика").save()
teacher_1 = Teacher(db_source=fs, fio='Петр Петрович', bio='учитель математики', contacts='petr@yandex.ru', office_id=415).save()
teacher_2 = Teacher(db_source=fs, fio='Павел Павлович', bio='учитель физики', contacts='pavel@yandex.ru', office_id=416).save()
group_1 = Group(db_source=fs, teacher_id=teacher_1.get_main_id(), class_letter="В", grade=10, profile_name="обычная математика").save()
group_2 = Group(db_source=fs, teacher_id=teacher_2.get_main_id(), class_letter="A", grade=11, profile_name="физикоматематический класс").save()
student_1 = Student(db_source=fs, full_name="Дмитрий", date_of_birth="01.03.02", contacts='+79099990930', bio=None).save()
student_2 = Student(db_source=fs, full_name="Юлия", date_of_birth="01.02.04", contacts='+79090001201', bio=None).save()
lesson_row_1 = LessonRow(db_source=fs, day_of_the_week='Пятница', group_id=group_1.get_main_id(), subject_id=subject_1.get_main_id(), room_id=416, start_time=1230, end_time=1315, timetable_id=1).save()
lesson_row_2 = LessonRow(db_source=fs,day_of_the_week='Понедельник', group_id=group_2.get_main_id(), subject_id=subject_2.get_main_id(), room_id=413, start_time=1030, end_time=1115, timetable_id=1).save()
lesson_row_3 = LessonRow(db_source=fs, day_of_the_week='Понедельник', group_id=group_2.get_main_id(), subject_id=subject_1.get_main_id(), room_id=412, start_time=930, end_time=1015, timetable_id=1).save()
lesson_row_4 = LessonRow(db_source=fs, day_of_the_week='Понедельник', group_id=group_1.get_main_id(), subject_id=subject_1.get_main_id(), room_id=416, start_time=945, end_time=1035, timetable_id=1).save()
lesson_row_1.append_teacher(teacher_1)
lesson_row_1.append_teacher(teacher_2)
lesson_row_2.append_teacher(teacher_2)
lesson_row_3.append_teacher(teacher_1)
lesson_row_4.append_teacher(teacher_2)
group_1.append_student(student_1)
group_2.append_student(student_2)

interface = CLI('../db')
interface.show_menu()

fs.delete('Subject', subject_1.get_main_id())
fs.delete('Subject', subject_2.get_main_id())
fs.delete('Teacher', teacher_1.get_main_id())
fs.delete('Teacher', teacher_2.get_main_id())
fs.delete('Group', group_1.get_main_id())
fs.delete('Group', group_2.get_main_id())
fs.delete('Student', student_1.get_main_id())
fs.delete('Student', student_2.get_main_id())
fs.delete('LessonRow', lesson_row_1.get_main_id())
fs.delete('LessonRow', lesson_row_2.get_main_id())