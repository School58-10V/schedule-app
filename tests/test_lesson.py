import datetime

from data_model.lesson import Lesson
from tests.team_AX_class_test_feature import test_function

example_1 = {'start_time': 1015, 'end_time': 1100, 'day': datetime.date.today(), 'teacher_id': 5,
             'group_id': 1, 'subject_id': 2, 'notes': 'Урок русского', 'state': True}
example_2 = {'start_time': 1100, 'end_time': 1145, 'day': datetime.date.today(), 'teacher_id': 7,
             'group_id': 1, 'subject_id': 1, 'notes': 'Урок математики', 'state': True}
example_1_update = {'end_time': 1030}
example_2_update = {'group_id': 3}
test_function(Lesson, example_1=example_1, example_2=example_2, example_1_update=example_1_update,
              example_2_update=example_2_update, csv_location='../data_examples/lesson.csv'
              )
