from data_model.group import Group
from data_model.student import Student
from db_source import DBSource

db_source = DBSource(host='postgresql.aakapustin.ru', user='schedule_app',
                     password='VYRL!9XEB3yXQs4aPz_Q', dbname='schedule_app')
# Создаем студента и сохраняем его
student = Student(db_source=db_source, date_of_birth='', full_name='Фио')
student.save()

# Создаем группу и сохраняем ее
group = Group(db_source=db_source, teacher_id=2, class_letter='', grade=3, profile_name=', ')
group.save()

# Создаем студента 1 и сохраняем его
student1 = Student(db_source=db_source, date_of_birth='', full_name='Ученик №1')
student1.save()

# Создаем группу 1 и сохраняем ее
group1 = Group(db_source=db_source, teacher_id=3, class_letter='А', grade=1, profile_name='Группа №1')
group1.save()

# Выводим всех изначальных студентов группы и все изначальные группы студентов
print('Было:', *group.get_all_students())
print('Было:', *student.get_all_groups())
print()

# Добавляем группы студенту и студентов в группу
student.append_group(group)
student.append_group(group1)
group.append_student(student)
group.append_student(student1)

# Добавляем повторно студента в группу, чтобы убедиться,
# что он его не добавляет, так как он уже есть
group.append_student(student)

# Выводим, что у нас получилось
print("Стало:", *group.get_all_students())
print("Стало,", *student.get_all_groups())
print()

# Удаляем группу у студента и студента из группы
student.remove_group(group)
group.remove_student(student1)

print('Стало снова:', *student.get_all_groups())
print("Стало снова:", *group.get_all_students())
print()

# Повторяем, чтобы показать, что второй раз он ничего не меняет
group.remove_student(student)
student.remove_group(group)

print("Стало:", *student.get_all_groups())
print("Стало:", *group.get_all_students())
