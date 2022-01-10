from data_model.subject import Subject
from tests.team_AX_class_test_feature import test_function

example_1 = {'subject_name': 'Алгебра'}
example_2 = {'subject_name': 'Теория вероятности'}
example_1_update = {'subject_name': 'Algebra'}
example_2_update = {'subject_name': 'Theory of chance'}
test_function(Subject, example_1=example_1, example_2=example_2, example_1_update=example_1_update,
              example_2_update=example_2_update, csv_location='../data_examples/subject_test.csv'
              )