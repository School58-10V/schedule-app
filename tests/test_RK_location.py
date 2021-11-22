from data_model.location import Location
from adapters.file_source import FileSource

a = FileSource()
a.insert('Location', {"location_type": "кабинет", "name": "213", "link": "None", "comment": "Математика"})
