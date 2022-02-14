import psycopg2
from psycopg2.extras import DictCursor
with psycopg2.connect(dbname='schedule_app', user='schedule_app',
                      password='VYRL!9XEB3yXQs4aPz_Q',
                      host='postgresql.aakapustin.ru') as conn:
    with conn.cursor(cursor_factory=DictCursor) as cursor:

        cursor.execute('''select l.subject_id from "Lessons" as l
                        join "LessonRows" as lr on l.object_id = lr.subject_id
                        join "TeachersForLessonRows" as tflr on tflr.lesson_row_id = lr.object_id
                        join "Teachers" as tc on tc.object_id = tflr.teacher_id
                        where
                        tc.fio = %s
                        and
                        l.day = %s ''', ("Хромов Михаил Романович", '2023-02-03', ))

        records = cursor.fetchall()
        print(*records, sep='')
cursor.close()
conn.close()

