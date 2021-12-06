from data_model.location import Location
from adapters.file_source import FileSource


file_source = FileSource()
location = Location.parse("../data_examples/location.csv")
print(*location)
for element in location:
    file_source.insert(type(element.get_model()).__name__, element.get_model().__dict__())

# file_source.insert('Location', {"location_type": "кабинет", "name": "258", "link": "None", "comment": "Физика"})
# file_source.insert('Location', {"location_type": "кабинет", "name": "290", "link": "None", "comment": "Астрономия"})
print(file_source.get_all('Location'))
print('удалили объект', file_source.delete('Location', 1041637850941617))
print('изменился ли айди?', file_source.update('Location', 1041637850941622, {"object_id": 1, "comment": 'Музыка'}))
print('еще один поменяли', file_source.update('Location', 1041638194031070, {"location_type": 'ссылка'}))
print('печатаем второй элемент', file_source.get_by_id('Location', 1041637850941622))
print(file_source.get_by_query('Location', {"type_of_location": 'кабинет'}), "печатаем все по кабинету")
print(file_source.get_all('Location'), 'печатаем все по заданию')
file_source.insert('Location', {"location_type": "ссылка", "name": "290", "link": "None", "comment": "Литература"})
print(file_source.get_all('Location'), 'печатаем все по заданию')