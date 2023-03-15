
from tests.team_AX_class_test_feature import test_function
from adapters.db_source import DBSource
from data_model.timetable import TimeTable

#example_1 = {"time_table_year": 2000}
#example_2 = {"time_table_year": 1}
#example_1_update = {"time_table_year": 2021}
#example_2_update = {"time_table_year": 2}
# test_function(TimeTable, example_1=example_1, example_2=example_2, example_1_update=example_1_update,
#              example_2_update=example_2_update, csv_location='../data_examples/timetable_test.csv'
#             )

db = DBSource(user='schedule_app', password='VYRL!9XEB3yXQs4aPz_Q', host='postgresql.aakapustin.ru')
tt = TimeTable(db)
tt1 = tt.get_by_id(54, db)
print(tt1.delete().__dict__())