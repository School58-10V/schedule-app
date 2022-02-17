from data_model.no_learning_period import NoLearningPeriod
from tests.team_AX_class_test_feature import test_function

example_1 = {'start': '01.01.2000', 'stop': '14.01.2000'}
example_2 = {'start': '12.02.2004', 'stop': '21.02.2004'}
example_1_update = {'start': '25.12.1999'}
example_2_update = {'stop': '10.02.2004'}
test_function(NoLearningPeriod, example_1=example_1, example_2=example_2, example_1_update=example_1_update,
              example_2_update=example_2_update, csv_location='../data_examples/group.csv'
              )
