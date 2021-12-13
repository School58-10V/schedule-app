from data_model.timetable import TimeTable
from tests.team_AX_class_test_feature import test_function

example_1 = {"time_table_year": 2000}
example_2 = {"time_table_year": 1}
example_1_update = {"time_table_year": 2021}
example_2_update = {"time_table_year": 2}
test_function(TimeTable, example_1=example_1, example_2=example_2, example_1_update=example_1_update,
              example_2_update=example_2_update, csv_location='../data_examples/timetable_test.csv'
              )