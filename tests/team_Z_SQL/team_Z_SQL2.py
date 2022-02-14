import psycopg2
from psycopg2.extras import DictCursor
with psycopg2.connect(dbname='schedule_app', user='smirnov',
                      password='ThfXckb@EvQ4zXqLm3Bb',
                      host='postgresql.aakapustin.ru') as conn:
    with conn.cursor(cursor_factory=DictCursor) as cursor:

        cursor.execute('''select l.subject_id from "Lessons" as l
                        join "LessonRows" as lr on l.object_id = lr.subject_id
                        join "TeachersForLessonRows" as tflr on tflr.lesson_row_id = lr.object_id
                        join "Teachers" as tc on tc.object_id = tflr.teacher_id
                        where
                        tc.fio = %s
                        and
                        l.day = '2023-02-03' ''', ("Хромов Михаил Романович", ))

        records = cursor.fetchall()
        print(*records, sep='')
cursor.close()
conn.close()

