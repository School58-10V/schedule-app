from data_model.location import Location

res = Location.parse("test_file.csv")
print(res[0])
loc1 = Location('Урок', 2, None, '', [])
loc1.save()
