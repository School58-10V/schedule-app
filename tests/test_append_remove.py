from data_model.teacher import Teacher
from data_model.lesson_row import LessonRow
from data_model.subject import Subject
from db_source import DBSource

db_source = DBSource(host='postgresql.aakapustin.ru', user='schedule_app',
                     password='VYRL!9XEB3yXQs4aPz_Q', dbname='schedule_app')
# Создаем учителя и сохраняем его
teacher = Teacher(db_source=db_source, fio='фио', bio='', contacts='', office_id=0)
teacher.save()

# Создаем ряд уровоков и сохраняем его
lesson_row = LessonRow(db_source=db_source, count_studying_hours=1, group_id=1, subject_id=1, room_id=1, start_time=1,
                       end_time=1, timetable_id=1)
lesson_row.save()

# Создаем ряд уроков 1 и сохраняем его
lesson_row1 = LessonRow(db_source=db_source, count_studying_hours=2, group_id=2, subject_id=2, room_id=2, start_time=2,
                        end_time=2, timetable_id=2)
lesson_row1.save()

# Создаём урок
subject = Subject(db_source=db_source, subject_name='матем', object_id=1)
subject.save()

# Создаём урок 1
subject1 = Subject(db_source=db_source, subject_name='русс яз', object_id=2)
subject.save()

# Добавляем группы студенту и студентов в группу
teacher.append_lesson_row(lesson_row)
