from data_model.lesson_row import LessonRow
from tests.team_AX_class_test_feature import test_function

example_1 = {'day_of_the_week': 'Friday', 'group_id': 1011641827322395, 'subject_id': 1081641829710171, 'room_id': 416, 'start_time': 1230, 'end_time': 1315, 'timetable_id': 1}
example_2 = {'day_of_the_week': 'Monday', 'group_id': 1011641827322391, 'subject_id': 1081641829710191, 'room_id': 413, 'start_time': 1030, 'end_time': 1115, 'timetable_id': 1}
example_1_update = {'day_of_the_week': 'Tuesday'}
example_2_update = {'subject_id': 1081641829710165}
test_function(LessonRow, example_1=example_1, example_2=example_2, example_1_update=example_1_update,
              example_2_update=example_2_update, csv_location='../data_examples/lesson_row.csv'
              )
