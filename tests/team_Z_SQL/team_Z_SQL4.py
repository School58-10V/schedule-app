import psycopg2
from psycopg2.extras import DictCursor
with psycopg2.connect(dbname='schedule_app', user='schedule_app',
                      password='VYRL!9XEB3yXQs4aPz_Q',
                      host='postgresql.aakapustin.ru') as conn:
    with conn.cursor(cursor_factory=DictCursor) as cursor:

        cursor.execute('''select st.full_name from "Subjects" as s
        join "LessonRows" as lr on lr.subject_id = s.object_id
        join "Groups" as gr on lr.group_id = gr.object_id
        join "StudentsForGroups" as sfg on sfg.group_id = gr.object_id
        join "Students" as st on st.object_id = sfg.student_id
        where
        s.name = %s ''', ("English", ))

        records = cursor.fetchall()
        print(*records, sep='')
cursor.close()
conn.close()
