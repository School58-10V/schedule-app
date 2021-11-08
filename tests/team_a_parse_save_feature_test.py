from data_model.lesson import Lesson
from data_model.group import Group

# сохранение Урока в файл .json
example_lesson = Lesson(9, 16, 3, 67, 8, 5, "")
print(example_lesson)
example_lesson.save('../db')

# чтение из .csv и сохранение Урока в файл .json
parsed_lesson = Lesson.parse('../data_examples/lesson.csv')[0][1]
print(parsed_lesson)
parsed_lesson.save('../db')

# сохранение Группы в файл .json
example_group = Group(6, "A", 7, "ФИЗМАТ")
print(example_group)
example_group.save('../db')

# чтение из .csv и сохранение Группы в файл .json
parsed_group = Group.parse("../data_examples/group.csv")[0][1]
print(parsed_group)
parsed_group.save('../db')
