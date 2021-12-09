from data_model.group import Group
from tests.team_AX_class_test_feature import test_function

example_1 = {'teacher_id': 10, 'class_letter': 'Б', 'grade': 10, 'profile_name': 'Математика'}
example_2 = {'teacher_id': 10, 'class_letter': 'А', 'grade': 10, 'profile_name': 'Математика'}
example_1_update = {'class_letter': 'В'}
example_2_update = {'profile_name': 'Русский Язык'}
test_function(Group, example_1=example_1, example_2=example_2, example_1_update=example_1_update,
              example_2_update=example_2_update, csv_location='../data_examples/group.csv'
              )