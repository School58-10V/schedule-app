from data_model.lesson import Lesson
from data_model.group import Group

lesson = Lesson(9, 16, 3, 67, 8, 5, "",)
lesson.save('../db')

lesson = Lesson()
lesson = lesson.parse('../data_examples/lesson_test.csv')[0]
print(lesson)
lesson.save('../db')

lesson = lesson[0][1]
print(lesson)
lesson.save('../db')
print()
print()

group = Group(6, "A", 7, "ФИЗМАТ")
group = group.parse("../data_examples/group_test.csv")[0]
print(group)
print(group)
group.save('../db')
print()
print()