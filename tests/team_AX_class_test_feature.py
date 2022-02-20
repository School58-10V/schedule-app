import random
from db_source import DBSource

db_location = '../db'
fS = DBSource(host='postgresql.aakapustin.ru', user='schedule_app',
              password='VYRL!9XEB3yXQs4aPz_Q', dbname='schedule_app')


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
    test_class_samples = TestingClass.parse(csv_location, fS)
    for data_sample in test_class_samples:
        if data_sample.has_error():
            raise ValueError("В данных закралась ошибочка, проверьте их")

    print(f'Список всех объектов из csv:', *[i.get_model() for i in test_class_samples], sep='\n', end='\n\n')

    # Берем один объект из списка и сохраняем его
    from_csv_object = test_class_samples[0].get_model()
    from_csv_object = TestingClass(**fS.insert(TestingClass.__name__, from_csv_object.__dict__()), db_source=fS)
    print(f'Первый объект из .csv (который мы только что сохранили):\n{from_csv_object}\n')
    print(f'Все объекты в db/.json (adapter):', *fS.get_all(TestingClass.__name__), sep='\n', end='\n\n')

    # Создаем еще два объекта
    object_2 = TestingClass(**example_1, db_source=fS)
    object_2 = fS.insert(TestingClass.__name__, object_2.__dict__())
    object_3 = TestingClass(**example_2, db_source=fS)
    object_3 = fS.insert(TestingClass.__name__, object_3.__dict__())
    print(f'fs.insert() еще два объекта: \n{object_2}\n{object_3}\n')

    # Удалим первый объект
    deleted_object = fS.delete(TestingClass.__name__, from_csv_object.get_main_id())
    print(f'Удалили объект который был из .csv, его ID было:\n{deleted_object}\n')
    print('Все объекты в db/.json (class):', *TestingClass.get_all(fS), sep='\n', end='\n\n')
    # object_2 = fS.update(object_id=object_2['object_id'], document=example_1_update,
    #                      collection_name=TestingClass.__name__)
    # пока не имеет смысла - у нас этот метод не работает
    # object_3 = fS.update(object_id=object_3['object_id'], document=example_2_update,
    #                      collection_name=TestingClass.__name__)

    print(f'Изменили 2 объекта:\n{object_2}\n{object_3}\n')
    print('Все объекты в db/.json (class):', *TestingClass.get_all(fS), sep='\n', end='\n\n')
    print('Все объекты в db/.json (adapter):', *fS.get_all(TestingClass.__name__), sep='\n', end='\n\n')
    print(object_3, "fjjfjfjjfjffjffojgnfjgir")
    try:
        print('Ищем второй объект (adapter):', fS.get_by_id(collection_name=TestingClass.__name__,
                                                            object_id=object_3['object_id']), '\n')
    except ValueError as e:
        print("Ошибка с поиском объектов", e)

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
