
from data_model.teachers_on_lesson_rows import TeachersOnLessonRows
from adapters.file_source import FileSource

fS = FileSource('../db')

# Берем список объектов из csv
teachers_on_lesson = TeachersOnLessonRows.parse('../data_examples/teachers_on_lesson_rows_test.csv')
print(f'Список всех объектов из csv', *[i[1] for i in teachers_on_lesson])
# Берем один объект из списка и сохраняем его
teacher_on_lesson = teachers_on_lesson[0][-1]
teacher_on_lesson = TeachersOnLessonRows(**fS.insert(TeachersOnLessonRows.__name__, teacher_on_lesson.__dict__()))
print(f'Первый объект: {teacher_on_lesson}\n')
print(f'Все объекты:', *fS.get_all(TeachersOnLessonRows.__name__))
# Создаем еще два объекта
teacher_on_lesson1 = TeachersOnLessonRows(teacher_id=5, lesson_row_id=10, object_id=5)
teacher_on_lesson1.save('../db')
teacher_on_lesson2 = TeachersOnLessonRows(teacher_id=4, lesson_row_id=10000, object_id=6)
teacher_on_lesson2.save('../db')
print(f'Еще два объекта: {teacher_on_lesson1}, {teacher_on_lesson2}\n')
# Удалим первый объект
teacher_on_lesson.delete('../db')
print(f'Удалили объект 1: {teacher_on_lesson}\n')

teacher_on_lesson1 = TeachersOnLessonRows(teacher_id=5, lesson_row_id=11, object_id=5)
fS.update(object_id=5, document=TeachersOnLessonRows(teacher_id=5, lesson_row_id=11, object_id=5).__dict__(),
          collection_name=TeachersOnLessonRows.__name__)
teacher_on_lesson2 = TeachersOnLessonRows(teacher_id=6, lesson_row_id=12, object_id=6)
fS.update(object_id=6, document=TeachersOnLessonRows(teacher_id=6, lesson_row_id=12, object_id=6).__dict__(),
          collection_name=TeachersOnLessonRows.__name__)

print(f'Изменили 2 объекта: {teacher_on_lesson1}; {teacher_on_lesson1} \n')
print('Все объекты через класс:', *TeachersOnLessonRows.get_all('../db'))
print('Список всех через адаптер: ', fS.get_all(TeachersOnLessonRows.__name__), '\n')
print('Ищем через адаптер: ', fS.get_by_id(collection_name=TeachersOnLessonRows.__name__,
                                           object_id=teacher_on_lesson2.get_main_id()))

print("Ищем через адаптер рандомный объект: ", fS.get_by_id(TeachersOnLessonRows.__name__,
                                                            2), end='\n\n')
print("Опять все файлы?", *fS.get_all(TeachersOnLessonRows.__name__))
fS.insert(TeachersOnLessonRows.__name__,
          TeachersOnLessonRows(teacher_id=1, lesson_row_id=3, object_id=None).__dict__())

print("Опять все файлы?", *fS.get_all(TeachersOnLessonRows.__name__))
