from data_model.lesson_row import LessonRow
from data_model.teacher import Teacher
from data_model.teachers_for_lesson_rows import TeachersForLessonRows as TFL
from db_source import DBSource

db = DBSource(host='postgresql.aakapustin.ru', user='schedule_app',
              password='VYRL!9XEB3yXQs4aPz_Q', dbname='schedule_app')

example_lesson_row = LessonRow(db_source=db, count_studying_hours=10, end_time=10, group_id=10,
                               room_id=10, start_time=10, subject_id=10, timetable_id=10).save()

example_teacher = Teacher(fio='а', bio='а', office_id=10, db_source=db).save()

print(f"Добавляю связь с {example_teacher.__dict__()}")

example_lesson_row.append_teacher(example_teacher)

example_lesson_row.append_teacher(example_teacher)

print(f'Файл со связями: {TFL.get_all(db_source=db)}')

print(f"Удаляю связь с {example_teacher.__dict__()}")

example_lesson_row.remove_teacher(example_teacher)

print(f'Файл со связями: {TFL.get_all(db_source=db)}')
