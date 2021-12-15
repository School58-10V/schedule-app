from data_model.timetable import TimeTable
from adapters.file_source import FileSource


def test_parse(db_source, subject, file_folder):
    all_object = subject.parse(file_folder, db_source)
    print(*[i.get_model() for i in all_object])
    return all_object


source = FileSource('../db')
timetables = test_parse(db_source=source, subject=TimeTable, file_folder='../data_examples/timetable_test.csv')