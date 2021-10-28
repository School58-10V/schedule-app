from data_model.location import Location


res = Location.parse("test_file.csv")
print(res[0])
