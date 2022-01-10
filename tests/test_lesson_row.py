from data_model.lesson_row import LessonRow
from tests.team_AX_class_test_feature import test_function

example_1 = {'count_studying_hours': 12, 'group_id': 101, 'subject_id': 102, 'room_id': 416, 'start_time': 1230, 'end_time': 1315, 'timetable_id': 1}
example_2 = {'count_studying_hours': 24, 'group_id': 102, 'subject_id': 105, 'room_id': 413, 'start_time': 1030, 'end_time': 1115, 'timetable_id': 1}
example_1_update = {'count_studying_hours': 36}
example_2_update = {'subject_id': 100238}
test_function(LessonRow, example_1=example_1, example_2=example_2, example_1_update=example_1_update,
              example_2_update=example_2_update, csv_location='../data_examples/lesson_row.csv'
              )
