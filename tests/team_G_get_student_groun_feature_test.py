# from data_model.group import Group
# from data_model.student import Student
# from adapters.file_source import FileSource
#
# # Создаем адаптор
# data = FileSource('../db')
# # Достаем студента с таким-то id
# try:
#     student = Student.get_by_id(1061638802407770, data)
#     # Берем все его группы
#     print(*student.get_all_groups())
#
# except ValueError:
#     print('Такого объекта нет')
#
# # Достаем группу с таким-то id
#
# try:
#     group = Group.get_by_id(1011638976291732, data)
#     # Берем всех его студентов
#     print(*group.get_all_students())
# except ValueError:
#     print('Такого объекта нет')
