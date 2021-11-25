import random

from data_model.teachers_on_lesson_rows import TeachersOnLessonRows
from adapters.file_source import FileSource
from data_model.timetable import TimeTable
from data_model.subject_lesson import Subject

fS = FileSource('../db')


def test_function(TestingClass, example_1: dict, example_2: dict,
                  example_1_update: dict, example_2_update: dict,
                  csv_location: str) -> None:
    """
    функция для полного теста класса, по стандарту который написал @TIlzziter
    
    **(возможно стоит переделать в функцию для каждого подпункта)
    
    :param TestingClass: класс, который будем тестировать
    :param example_1: пример первого объекта (словарь аргументов)
    :param example_2: пример второго объекта (словарь аргументов)
    :param example_1_update: пример изменения данных первого аргумента
    :param example_2_update: пример изменения данных второго аргумента
    :param csv_location: путь до .csv файла 
    :return: ничего
    """

    print(f'------ НАЧАЛО ТЕСТ КЛАССА {TestingClass.__name__} ------\n')

    # Берем список объектов из csv
    teachers_on_lesson = TestingClass.parse(csv_location)
    print(f'Список всех объектов из csv:', *[i[1] for i in teachers_on_lesson], sep='\n', end='\n\n')

    # Берем один объект из списка и сохраняем его
    from_csv_object = teachers_on_lesson[0][-1]
    from_csv_object = TestingClass(**fS.insert(TestingClass.__name__, from_csv_object.__dict__()))
    print(f'Первый объект из .csv (который мы только что сохранили):\n{from_csv_object}\n')
    print(f'Все объекты в db/.json (adapter):', *fS.get_all(TestingClass.__name__), sep='\n', end='\n\n')

    # Создаем еще два объекта
    object_2 = TestingClass(**example_1)
    object_2 = fS.insert(TestingClass.__name__, object_2.__dict__())
    object_3 = TestingClass(**example_2)
    object_3 = fS.insert(TestingClass.__name__, object_3.__dict__())
    print(f'fs.insert() еще два объекта: \n{object_2}\n{object_3}\n')

    # Удалим первый объект
    from_csv_object.delete('../db')
    print(f'Удалили объект который был из .csv (id=None теперь):\n{from_csv_object}\n')
    print('Все объекты в db/.json (class):', *TestingClass.get_all('../db'), sep='\n', end='\n\n')
    object_2 = fS.update(object_id=object_2['object_id'], document=example_1_update, collection_name=TestingClass.__name__)

    object_3 = fS.update(object_id=object_3['object_id'], document=example_2_update, collection_name=TestingClass.__name__)

    print(f'Изменили 2 объекта:\n{object_2}\n{object_3}\n')
    print('Все объекты в db/.json (class):', *TestingClass.get_all('../db'), sep='\n', end='\n\n')
    print('Все объекты в db/.json (adapter):', *fS.get_all(TestingClass.__name__), sep='\n', end='\n\n')
    print('Ищем второй объект (adapter):', fS.get_by_id(collection_name=TestingClass.__name__,
                                                        object_id=object_3['object_id']), '\n')

    random_existing_id = random.choice(fS.get_all(TestingClass.__name__))['object_id']
    print(f"Рандомный объект полученный по ID(={random_existing_id} (adapter):",
          fS.get_by_id(TestingClass.__name__, random_existing_id), end='\n\n')

    print("Все файлы (adapter):", *fS.get_all(TestingClass.__name__), sep='\n', end='\n\n')

    fS.insert(TestingClass.__name__, from_csv_object.__dict__())
    print("Вернули первый объект, все файлы (adapter):", *fS.get_all(TestingClass.__name__), sep='\n')

    print(f'------ КОНЕЦ ТЕСТА КЛАССА {TestingClass.__name__} ------\n\n')


example_1 = {"teacher_id": 5, "lesson_row_id": 10, "object_id": 5}
example_2 = {"teacher_id": 4, "lesson_row_id": 10000, "object_id": 6}
example_1_update = {"teacher_id": 15, "lesson_row_id": 123}
example_2_update = {"teacher_id": 25, "lesson_row_id": 999}
test_function(TeachersOnLessonRows, example_1=example_1, example_2=example_2,
              example_1_update=example_1_update, example_2_update=example_2_update,
              csv_location='../data_examples/teachers_on_lesson_rows_test.csv',
              )

# print('\n\nНовый класс!!!!!!!!!!!')
# timetables = TimeTable.parse('../data_examples/timetable_test.csv')
# print(f'Список всех объектов из csv', *[i[1] for i in timetables])
# # Берем один объект из списка и сохраняем его
# timetable = timetables[0][-1]
# timetable = TimeTable(**fS.insert(TimeTable.__name__, timetable.__dict__()))
# print(f'Первый объект: {timetable}\n')
# print(f'Все объекты:', *fS.get_all(TimeTable.__name__))
# # Создаем еще два объекта
# timetable1 = TimeTable(object_id=5, time_table_year=2000)
# timetable1.save('../db')
# timetable2 = TimeTable(time_table_year=1, object_id=6)
# timetable2.save('../db')
# print(f'Еще два объекта: {timetable1}, {timetable2}\n')
# # Удалим первый объект
# timetable.delete('../db')
# print(f'Удалили объект 1: {timetable}\n')
# print('Все объекты:', *TimeTable.get_all('../db'))
# timetable1 = TimeTable(time_table_year=2011, object_id=5)
# fS.update(object_id=5, document=timetable1.__dict__(),
#           collection_name=TimeTable.__name__)
# timetable2 = TimeTable(time_table_year=112121212121121211, object_id=6)
# fS.update(object_id=6, document=timetable2.__dict__(),
#           collection_name=TimeTable.__name__)
#
# print(f'Изменили 2 объекта: {timetable1}; {timetable2} \n')
# print('Все объекты через класс:', *TimeTable.get_all('../db'))
# print('Список всех через адаптер: ', fS.get_all(TimeTable.__name__), '\n')
# print('Ищем через адаптер: ', fS.get_by_id(collection_name=TimeTable.__name__,
#                                            object_id=timetable2.get_main_id()))
#
# print("Ищем через адаптер рандомный объект: ", fS.get_by_id(TimeTable.__name__,
#                                                             2), end='\n\n')
# print("Опять все файлы?", *fS.get_all(TimeTable.__name__))
# fS.insert(TimeTable.__name__,
#           TimeTable(time_table_year=2005, object_id=None).__dict__())
#
# print("Опять все файлы?", *fS.get_all(TimeTable.__name__))
#
# subject_lessons = Subject.parse('../data_examples/timetable_test.csv')
# print(f'Список всех объектов из csv', *[i[1] for i in subject_lessons])
# # Берем один объект из списка и сохраняем его
# subject_lesson = subject_lessons[0][-1]
# subject_lesson = Subject(**fS.insert(Subject.__name__, subject_lesson.__dict__()))
# print(f'Первый объект: {subject_lesson}\n')
# print(f'Все объекты:', *fS.get_all(Subject.__name__))
# # Создаем еще два объекта
# subject_lesson1 = Subject(object_id=5, subject_name="Algebra")
# subject_lesson1.save('../db')
# subject_lesson2 = Subject(subject_name="Physics", object_id=6)
# subject_lesson2.save('../db')
# print(f'Еще два объекта: {subject_lesson1}, {subject_lesson2}\n')
# # Удалим первый объект
# subject_lesson.delete('../db')
# print(f'Удалили объект 1: {subject_lesson}\n')
# print('Все объекты:', *Subject.get_all('../db'))
# subject_lesson1 = Subject(subject_name="PE", object_id=5)
# fS.update(object_id=5, document=subject_lesson1.__dict__(),
#           collection_name=Subject.__name__)
# subject_lesson2 = Subject(subject_name="Eng", object_id=6)
# fS.update(object_id=6, document=subject_lesson2.__dict__(),
#           collection_name=Subject.__name__)
#
# print(f'Изменили 2 объекта: {subject_lesson1}; {subject_lesson2} \n')
# print('Все объекты через класс:', *Subject.get_all('../db'))
# print('Список всех через адаптер: ', fS.get_all(Subject.__name__), '\n')
# print('Ищем через адаптер: ', fS.get_by_id(collection_name=Subject.__name__,
#                                            object_id=subject_lesson2.get_main_id()))
#
# print("Ищем через адаптер рандомный объект: ", fS.get_by_id(Subject.__name__,
#                                                             2), end='\n\n')
# print("Опять все файлы?", *fS.get_all(Subject.__name__))
# fS.insert(Subject.__name__,
#           Subject(subject_name="Geometry", object_id=None).__dict__())
#
# print("Опять все файлы?", *fS.get_all(Subject.__name__))
