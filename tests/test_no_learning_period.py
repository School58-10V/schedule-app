from data_model.no_learning_period import NoLearningPeriod
from tests.team_AX_class_test_feature import test_function

example_1 = {'start_time': '2000-01-01', 'stop_time': '2000-01-14', 'timetable_id': 10}
example_2 = {'start_time': '2004-02-12', 'stop_time': '2004-02-21', 'timetable_id': 10}
example_1_update = {'start_time': '1999-12-25'}
example_2_update = {'stop_time': '2004-02-10'}
test_function(NoLearningPeriod, example_1=example_1, example_2=example_2, example_1_update=example_1_update,
              example_2_update=example_2_update, csv_location='../data_examples/no_learning_period.csv'
              )  # А почему тут была ссылка на Group.csv!?
