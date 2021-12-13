import random

from data_model.teacher import Teacher
from data_model.teachers_for_lesson_rows import TeachersForLessonRows
from adapters.file_source import FileSource
from data_model.timetable import TimeTable
from data_model.subject import Subject
from data_model.parsed_data import ParsedData

db_location = '../db'
fS = FileSource(db_location)


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
    test_class_samples = TestingClass.parse(csv_location)
    for data_sample in test_class_samples:
        if data_sample.has_error():
            raise ValueError("В данных закралась ошибочка, проверьте их")

    print(f'Список всех объектов из csv:', *[i.get_model() for i in test_class_samples], sep='\n', end='\n\n')

    # Берем один объект из списка и сохраняем его
    from_csv_object = test_class_samples[0].get_model()
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
    deleted_object = fS.delete(TestingClass.__name__, from_csv_object.get_main_id())
    print(f'Удалили объект который был из .csv, его ID было:\n{deleted_object}\n')
    print('Все объекты в db/.json (class):', *TestingClass.get_all('../db'), sep='\n', end='\n\n')
    object_2 = fS.update(object_id=object_2['object_id'], document=example_1_update,
                         collection_name=TestingClass.__name__)

    object_3 = fS.update(object_id=object_3['object_id'], document=example_2_update,
                         collection_name=TestingClass.__name__)

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
    print("Убираем все объекты из файла...")
    for i in fS.get_all(TestingClass.__name__):
        fS.delete(TestingClass.__name__, i['object_id'])

    print(f'\n------ КОНЕЦ ТЕСТА КЛАССА {TestingClass.__name__} ------\n\n')


example_1 = {"teacher_id": 5, "lesson_row_id": 10, "object_id": 5}
example_2 = {"teacher_id": 4, "lesson_row_id": 10000, "object_id": 6}
example_1_update = {"teacher_id": 15, "lesson_row_id": 123}
example_2_update = {"teacher_id": 25, "lesson_row_id": 999}
test_function(TeachersForLessonRows, example_1=example_1, example_2=example_2,
              example_1_update=example_1_update, example_2_update=example_2_update,
              csv_location='../data_examples/teachers_for_lesson_rows_test.csv',
              )

example_1 = {"time_table_year": 2000}
example_2 = {"time_table_year": 1}
example_1_update = {"time_table_year": 2021}
example_2_update = {"time_table_year": 2}
test_function(TimeTable, example_1=example_1, example_2=example_2, example_1_update=example_1_update,
              example_2_update=example_2_update, csv_location='../data_examples/timetable_test.csv'
              )

example_1 = {'subject_name': 'Алгебра'}
example_2 = {'subject_name': 'Теория вероятности'}
example_1_update = {'subject_name': 'Algebra'}
example_2_update = {'subject_name': 'Theory of chance'}
test_function(Subject, example_1=example_1, example_2=example_2, example_1_update=example_1_update,
              example_2_update=example_2_update, csv_location='../data_examples/subject_test.csv'
              )

example_1 = {'fio': 'Афанасьев Александр Николаевич', 'bio': 'учитель инфы', 'contacts': '*контакты*', 'office_id': 12,
             'subject': 'Информатика'}
example_2 = {'fio': 'Капустин Андрей Андреевич', 'bio': 'учитель инфы', 'contacts': '*контакты*', 'office_id': 12,
             'subject': 'Информатика'}
example_1_update = {'office_id': 13}
example_2_update = {'office_id': 13}
test_function(Teacher, example_1=example_1, example_2=example_2, example_1_update=example_1_update,
              example_2_update=example_2_update, csv_location='../data_examples/teacher.csv'
              )
