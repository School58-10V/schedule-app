from data_model.location import Location
from adapters.file_source import FileSource

# Создание файла сохранения Location

test1_class = Location('Урок', 2, 3, '', [])
test1_class.save()
test1_class = Location('Пара', 3, 8, '', [])
test1_class.save()

# Тесты для метода get_by_all

test2_class = FileSource()
print(test2_class.get_all("Location"))

# Тесты для метода get_by_id
