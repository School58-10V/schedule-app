from data_model.group import Group
from data_model.student import Student
from adapters.file_source import FileSource

db_source = FileSource('../db')
student = Student(db_source=db_source, date_of_birth='', full_name='Фио')
student.save()
group = Group(db_source=db_source, teacher_id=2, class_letter='', grade=3, profile_name=', ')
group.save()
print('Было:', *group.get_all_students())
print('Было:', *student.get_all_groups())
student.append_group(group)
group.append_student(student)
print("Стало:", *group.get_all_students())
print("Стало,", *student.get_all_groups())
group.delete_student(student)
student.delete_group(group)
print("Стало:", *group.get_all_students())
print("Стало,", *student.get_all_groups())
