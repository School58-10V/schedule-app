from adapters.file_source import FileSource
from data_model.lesson_row import LessonRow
from data_model.teacher import Teacher

db = FileSource(db_path='../db')

example_lesson_row = LessonRow(db_source=db, count_studying_hours=10, end_time=10, group_id=10,
                               room_id=10, start_time=10, subject_id=10, timetable_id=10).save()

example_teacher = Teacher(fio='а', bio='а', office_id=10, db_source=db).save()

print(f"Добавляю связь с {example_teacher.__dict__()}")

example_lesson_row.append_teacher(example_teacher)

print(f'Файл со связями: {db.get_all("SubjectsAndTeachers")}')

print(f"Удаляю связь с {example_teacher.__dict__()}")

example_lesson_row.remove_teacher(example_teacher)

print(f'Файл со связями: {db.get_all("SubjectsAndTeachers")}')
