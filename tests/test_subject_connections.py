from adapters.file_source import FileSource
from data_model.subject import Subject
from data_model.teacher import Teacher
db = FileSource(db_path='../db')
example_teacher = Teacher(fio='Name Surname', bio='математик', office_id=12, db_source=db).save()
example_subject = Subject(subject_name='Алгебра', db_source=db).save()
example_subject.append_teacher(example_teacher)
example_subject.delete_teacher(example_teacher)