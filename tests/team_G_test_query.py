import psycopg2


conn = psycopg2.connect(dbname='schedule_app', user='kuranova',
                        password='s9iz.4c-yC-LREFf_63_', host='postgresql.aakapustin.ru')
cursor = conn.cursor()

cursor.execute('''select count (distinct lr.object_id) from
"Teachers" as tc
join "TeachersForLessonRows" as tlr on tlr.teacher_id = tc.object_id
join "LessonRows" as lr on lr.object_id = tlr.lesson_row_id
where
lr.day_of_the_week = 'пятница'
and
tc.fio = 'Антон Антонович Антонов'
and
lr.start_time > 1000''')
records = cursor.fetchall()

cursor.close()
conn.close()
print(records)
