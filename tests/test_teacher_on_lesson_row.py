from data_model.teachers_on_lesson_rows import TeachersOnLessonRows
from tests.team_AX_class_test_feature import test_function

example_1 = {"teacher_id": 5, "lesson_row_id": 10, "object_id": 5}
example_2 = {"teacher_id": 4, "lesson_row_id": 10000, "object_id": 6}
example_1_update = {"teacher_id": 15, "lesson_row_id": 123}
example_2_update = {"teacher_id": 25, "lesson_row_id": 999}
test_function(TeachersOnLessonRows, example_1=example_1, example_2=example_2,
              example_1_update=example_1_update, example_2_update=example_2_update,
              csv_location='../data_examples/teachers_on_lesson_rows_test.csv',
              )