import psycopg2
from psycopg2.extras import DictCursor
with psycopg2.connect(dbname='schedule_app', user='smirnov',
                      password='ThfXckb@EvQ4zXqLm3Bb',
                      host='postgresql.aakapustin.ru') as conn:
    with conn.cursor(cursor_factory=DictCursor) as cursor:

        cursor.execute('''select s.name from "Subjects" as s
                join "LessonRows" as lr on lr.subject_id = s.object_id
                join "TimeTables" as tt on tt.object_id = lr.timetable_id
                join "Groups" as gr on gr.object_id = lr.group_id
                join "StudentsForGroups" as sfg on sfg.group_id = gr.object_id
                join "Students" as st on st.object_id = sfg.student_id
                where st.full_name = %s and tt.time_table_year = %s ''', ("Хромов Михаил Романович", 2020, ))

        records = cursor.fetchall()
        print(*records, sep='')
cursor.close()
conn.close()
