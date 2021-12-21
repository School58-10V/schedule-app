from data_model.group import Group
from data_model.student import Student
from adapters.file_source import FileSource

db_source = FileSource('../db')
student = Student(db_source=db_source, date_of_birth='', full_name='Фио')
student.save()

group = Group(db_source=db_source, teacher_id=2, class_letter='', grade=3, profile_name=', ')
group.save()

student1 = Student(db_source=db_source, date_of_birth='', full_name='Ученик №1')
student1.save()

group1 = Group(db_source=db_source, teacher_id=3, class_letter='А', grade=1, profile_name='Группа №1')
group1.save()

print('Было:', *group.get_all_students())
print('Было:', *student.get_all_groups())

student.append_group(group)
student.append_group(group1)
group.append_student(student)
group.append_student(student1)
group.append_student(student)

print("Стало:", *group.get_all_students())
print("Стало,", *student.get_all_groups())

student.remove_group(group)
group.remove_student(student)

print('Стало снова:', *student.get_all_groups())
print("Стало снова:", *group.get_all_students())

group.remove_student(student)
student.remove_group(group)

print("Стало:", *group.get_all_students())
print("Стало,", *student.get_all_groups())
