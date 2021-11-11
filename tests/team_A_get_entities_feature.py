from data_model.lesson import Lesson
from data_model.group import Group

# Тесты для Урока
get_all = Lesson.get_all('../data_examples')
get_by_id = Lesson.get_by_id(2, '../data_examples')
print(f'Методы Lesson.get_all() и Lesson.get_by_id(): {get_all}, {get_by_id}')

try:
    Lesson.get_by_id(1234567890, '../data_examples')
except ValueError as e:
    print(e)

print()

# Тесты для группы
get_all = Group.get_all('../data_examples')
get_by_id = Group.get_by_id(3, '../data_examples')
print(f'Методы Group.get_all() и Group.get_by_id(): {get_all}, {get_by_id}')

try:
    Lesson.get_by_id(1234567890, '../data_examples')
except ValueError as e:
    print(e)
