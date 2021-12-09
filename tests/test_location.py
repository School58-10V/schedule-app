from data_model.location import Location
from tests.team_AX_class_test_feature import test_function

example_1 = {"location_type": "кабинет", "name": "268", "link": "None", "comment": "Русский язык"}
example_2 = {"location_type": "кабинет", "name": "231", "link": "None", "comment": "Математика"}
example_1_update = {'location_type': 'Ссылка'}
example_2_update = {'comment': 'Физика'}
test_function(Location, example_1=example_1, example_2=example_2, example_1_update=example_1_update,
              example_2_update=example_2_update, csv_location='../data_examples/location.csv'
              )
