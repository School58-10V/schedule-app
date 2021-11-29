from data_model.location import Location
from adapters.file_source import FileSource


# Создание файла сохранения Location

def fill_test_file():
    with open('../db/Location.json', 'wb'):
        pass
    test1_class = Location('Урок', 1, 3, '', [])
    test1_class.save()
    test1_class = Location('Пара', 2, 8, '', [])
    test1_class.save()


def space():
    print("\n")


# Тесты для метода get_by_all

fill_test_file()
test2_class = FileSource()
print("Пример работы метода get_all:")
for i in test2_class.get_all("Location"): print(i)
space()

# Тесты для метода get_by_id

fill_test_file()
test2_class = FileSource()
print("Пример работы метода get_by_id:")
print("Мы берем из данного списка:")
for i in test2_class.get_all("Location"): print(i)
print("Ровно один элемент по указанному при вызове ID:")
print(test2_class.get_by_id("Location", 2))
space()

# Тесты для методов update и delete

test3_class = FileSource()
print(test3_class.get_all('Location'))
test3_class.update('Location', 1041637588222989, {"comment": "Математика и Физика"})
print(test3_class.get_all('Location'))
test3_class.delete('Location', 1041637588222989)
print(test3_class.get_all('Location'))
space()
