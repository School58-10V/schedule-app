from data_model.teacher import Teacher
from tests.team_AX_class_test_feature import test_function

example_1 = {'fio': 'Афанасьев Александр Николаевич', 'bio': 'учитель инфы', 'contacts': '*контакты*', 'office_id': 12,
             'subject': 'Информатика'}
example_2 = {'fio': 'Капустин Андрей Андреевич', 'bio': 'учитель инфы', 'contacts': '*контакты*', 'office_id': 12,
             'subject': 'Информатика'}
example_1_update = {'office_id': 13}
example_2_update = {'office_id': 13}
test_function(Teacher, example_1=example_1, example_2=example_2, example_1_update=example_1_update,
              example_2_update=example_2_update, csv_location='../data_examples/teacher.csv'
              )