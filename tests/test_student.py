import datetime

from data_model.student import Student
from tests.team_AX_class_test_feature import test_function

example_1 = {"full_name": "Ученик 1", "date_of_birth": datetime.date.today()}
example_2 = {"full_name": "Ученик 2", "date_of_birth": datetime.date.today()}
example_1_update = {"full_name": "Ученик 4"}
example_2_update = {"full_name": "Ученик 3"}
test_function(Student, example_1=example_1, example_2=example_2, example_1_update=example_1_update,
              example_2_update=example_2_update, csv_location='../data_examples/student.csv'
              )
