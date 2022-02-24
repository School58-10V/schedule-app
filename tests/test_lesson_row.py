from data_model.lesson_row import LessonRow
from tests.team_AX_class_test_feature import test_function

example_1 = {'day_of_the_week': "пятница", 'group_id': 1, 'subject_id': 2, 'room_id': 6, 'start_time': 1230,
             'end_time': 1315, 'timetable_id': 1}
example_2 = {'day_of_the_week': "вторник", 'group_id': 2, 'subject_id': 1, 'room_id': 3, 'start_time': 1030,
             'end_time': 1115, 'timetable_id': 1}
example_1_update = {'day_of_the_week': "среда"}
example_2_update = {'subject_id': 1}
test_function(LessonRow, example_1=example_1, example_2=example_2, example_1_update=example_1_update,
              example_2_update=example_2_update, csv_location='../data_examples/lesson_row.csv'
              )
