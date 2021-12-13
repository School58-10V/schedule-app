from data_model.subject_lesson import Subject
from tests.team_AX_class_test_feature import test_function

example_1 = {'subject_name': 'Изобразительное Искусство'}
example_2 = {'subject_name': 'Родной язык и литература'}
example_1_update = {'subject_name': 'МХК'}
example_2_update = {'subject_name': 'Русский Язык'}
test_function(Subject, example_1=example_1, example_2=example_2, example_1_update=example_1_update,
              example_2_update=example_2_update, csv_location='../data_examples/subject_lesson.csv'
              )