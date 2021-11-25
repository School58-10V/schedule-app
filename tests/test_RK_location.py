from data_model.location import Location
from data_model.abstract_model import AbstractModel
from adapters.file_source import FileSource


file_source = FileSource()
location = Location.parse("../data_examples/location.csv")
print(*location)
location_list = []
for element in location:
    if not element.has_error():
        file_source.insert(type(element.get_model()).__name__, element.get_model().__dict__())

# file_source.insert('Location', {"location_type": "кабинет", "name": "258", "link": "None", "comment": "Физика"})
# file_source.insert('Location', {"location_type": "кабинет", "name": "290", "link": "None", "comment": "Астрономия"})

