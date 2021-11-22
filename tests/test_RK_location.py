from data_model.location import Location
from adapters.file_source import FileSource

a = FileSource()
# a.insert('Location', {"location_type": "кабинет", "name": "213", "link": "None", "comment": "Математика"})

# комментарий, так как я его уже себе добавила и теперь у меня есть его айди. На вашем устройстве придется
# его перезаписать и проверить его айди.

print(a.get_by_id('Location', 1041637588222989)) # у меня работает
# a.insert('Location', {"location_type": "кабинет", "name": "228", "link": "None", "comment": "Русский Язык"})

# та же ситуация, что и с прошлым инсертом
print(a.get_all('Location'))
a.update('Location', 1041637588222989, {"comment": "Математика и Физика"})
print(a.get_all('Location'))
a.delete('Location', 1041637588222989)
print(a.get_all('Location'))