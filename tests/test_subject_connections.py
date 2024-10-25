from adapters.db_source import DBSource
from data_model.subject import Subject
from data_model.teacher import Teacher
db = DBSource(host='postgresql.aakapustin.ru', user='schedule_app',
              password='VYRL!9XEB3yXQs4aPz_Q', dbname='schedule_app')
example_teacher = Teacher(fio='Name Surname', bio='математик', office_id=12, db_source=db).save()
example_subject = Subject(subject_name='Алгебра', db_source=db).save()
print(f"Добавляем связь с {example_teacher.__dict__()}")
example_subject.append_teacher(example_teacher)
print(f'Теперь наш файл со связями: {db.get_all("SubjectsAndTeachers")}')
print(f"Удаляем связь с {example_teacher.__dict__()}")
example_subject.remove_teacher(example_teacher)
print(f'Теперь наш файл со связями: {db.get_all("SubjectsAndTeachers")}')
