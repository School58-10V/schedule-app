
from data_model.teachers_on_lesson_rows import TeachersOnLessonRows
from adapters.file_source import FileSource
from data_model.timetable import TimeTable
from data_model.subject_lesson import Subject

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
print('Все объекты:', *TeachersOnLessonRows.get_all('../db'))
teacher_on_lesson1 = TeachersOnLessonRows(teacher_id=5, lesson_row_id=11, object_id=5)
fS.update(object_id=5, document=TeachersOnLessonRows(teacher_id=5, lesson_row_id=11, object_id=5).__dict__(),
          collection_name=TeachersOnLessonRows.__name__)
teacher_on_lesson2 = TeachersOnLessonRows(teacher_id=6, lesson_row_id=12, object_id=6)
fS.update(object_id=6, document=TeachersOnLessonRows(teacher_id=6, lesson_row_id=12, object_id=6).__dict__(),
          collection_name=TeachersOnLessonRows.__name__)

print(f'Изменили 2 объекта: {teacher_on_lesson1}; {teacher_on_lesson2} \n')
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

print('\n\nНовый класс!!!!!!!!!!!')
timetables = TimeTable.parse('../data_examples/timetable_test.csv')
print(f'Список всех объектов из csv', *[i[1] for i in timetables])
# Берем один объект из списка и сохраняем его
timetable = timetables[0][-1]
timetable = TimeTable(**fS.insert(TimeTable.__name__, timetable.__dict__()))
print(f'Первый объект: {timetable}\n')
print(f'Все объекты:', *fS.get_all(TimeTable.__name__))
# Создаем еще два объекта
timetable1 = TimeTable(object_id=5, time_table_year=2000)
timetable1.save('../db')
timetable2 = TimeTable(time_table_year=1, object_id=6)
timetable2.save('../db')
print(f'Еще два объекта: {timetable1}, {timetable2}\n')
# Удалим первый объект
timetable.delete('../db')
print(f'Удалили объект 1: {timetable}\n')
print('Все объекты:', *TimeTable.get_all('../db'))
timetable1 = TimeTable(time_table_year=2011, object_id=5)
fS.update(object_id=5, document=timetable1.__dict__(),
          collection_name=TimeTable.__name__)
timetable2 = TimeTable(time_table_year=112121212121121211, object_id=6)
fS.update(object_id=6, document=timetable2.__dict__(),
          collection_name=TimeTable.__name__)

print(f'Изменили 2 объекта: {timetable1}; {timetable2} \n')
print('Все объекты через класс:', *TimeTable.get_all('../db'))
print('Список всех через адаптер: ', fS.get_all(TimeTable.__name__), '\n')
print('Ищем через адаптер: ', fS.get_by_id(collection_name=TimeTable.__name__,
                                           object_id=timetable2.get_main_id()))

print("Ищем через адаптер рандомный объект: ", fS.get_by_id(TimeTable.__name__,
                                                            2), end='\n\n')
print("Опять все файлы?", *fS.get_all(TimeTable.__name__))
fS.insert(TimeTable.__name__,
          TimeTable(time_table_year=2005, object_id=None).__dict__())

print("Опять все файлы?", *fS.get_all(TimeTable.__name__))


subject_lessons = Subject.parse('../data_examples/timetable_test.csv')
print(f'Список всех объектов из csv', *[i[1] for i in subject_lessons])
# Берем один объект из списка и сохраняем его
subject_lesson = subject_lessons[0][-1]
subject_lesson = Subject(**fS.insert(Subject.__name__, subject_lesson.__dict__()))
print(f'Первый объект: {subject_lesson}\n')
print(f'Все объекты:', *fS.get_all(Subject.__name__))
# Создаем еще два объекта
subject_lesson1 = Subject(object_id=5, subject_name="Algebra")
subject_lesson1.save('../db')
subject_lesson2 = Subject(subject_name="Physics", object_id=6)
subject_lesson2.save('../db')
print(f'Еще два объекта: {subject_lesson1}, {subject_lesson2}\n')
# Удалим первый объект
subject_lesson.delete('../db')
print(f'Удалили объект 1: {subject_lesson}\n')
print('Все объекты:', *Subject.get_all('../db'))
subject_lesson1 = Subject(subject_name="PE", object_id=5)
fS.update(object_id=5, document=subject_lesson1.__dict__(),
          collection_name=Subject.__name__)
subject_lesson2 = Subject(subject_name="Eng", object_id=6)
fS.update(object_id=6, document=subject_lesson2.__dict__(),
          collection_name=Subject.__name__)

print(f'Изменили 2 объекта: {subject_lesson1}; {subject_lesson2} \n')
print('Все объекты через класс:', *Subject.get_all('../db'))
print('Список всех через адаптер: ', fS.get_all(Subject.__name__), '\n')
print('Ищем через адаптер: ', fS.get_by_id(collection_name=Subject.__name__,
                                           object_id=subject_lesson2.get_main_id()))

print("Ищем через адаптер рандомный объект: ", fS.get_by_id(Subject.__name__,
                                                            2), end='\n\n')
print("Опять все файлы?", *fS.get_all(Subject.__name__))
fS.insert(Subject.__name__,
          Subject(subject_name="Geometry", object_id=None).__dict__())

print("Опять все файлы?", *fS.get_all(Subject.__name__))
