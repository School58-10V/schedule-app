from data_model.timetable import TimeTable
from adapters.file_source import FileSource
# from data_model.teachers_for_subjects import TeachersForSubjects
from data_model.teachers_for_lesson_rows import TeachersForLessonRows
from data_model.location import Location
from data_model.teacher import Teacher
from data_model.subject import Subject
from data_model.student import Student
from data_model.lesson import Lesson
from data_model.lesson_row import LessonRow
from data_model.no_learning_period import NoLearningPeriod


def test_parse(db_source, subject, file_folder):
    all_object = subject.parse(file_folder, db_source)
    print(*[i.get_model() for i in all_object])
    return all_object


source = FileSource('../db')

timetables = test_parse(db_source=source, subject=TimeTable, file_folder='../data_examples/timetable_test.csv')

# teachers_for_lesson_rows = test_parse(source, TeachersForLessonRows,
#                                       '../data_examples/teachers_for_lesson_rows_test.csv')

locations = test_parse(source, Location, '../data_examples/location.csv')

teachers = test_parse(source, Teacher, '../data_examples/teacher.csv')

subjects = test_parse(source, Subject, '../data_examples/subject_test.csv')

students = test_parse(source, Student, '../data_examples/student.csv')

no_learning_periods = test_parse(source, NoLearningPeriod, '../data_examples/no_learning_period.csv')

lesson_rows = test_parse(source, LessonRow, '../data_examples/lesson_row.csv')

lessons = test_parse(source, Lesson, '../data_examples/lesson.csv')