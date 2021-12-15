from data_model.timetable import TimeTable
from data_model.location import Location
from data_model.subject import Subject
from data_model.student import Student
from data_model.no_learning_period import NoLearningPeriod
from adapters.file_source import FileSource


def test_parse(db_source, subject, file_folder):
    all_object = subject.parse(file_folder, db_source)
    print(*[i.get_model() for i in all_object])
    return all_object


source = FileSource('../db')
timetables = test_parse(db_source=source, subject=Student, file_folder='../data_examples/student.csv')
