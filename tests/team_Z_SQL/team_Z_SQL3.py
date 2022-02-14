import psycopg2
from psycopg2.extras import DictCursor
with psycopg2.connect(dbname='schedule_app', user='smirnov',
                      password='ThfXckb@EvQ4zXqLm3Bb',
                      host='postgresql.aakapustin.ru') as conn:
    with conn.cursor(cursor_factory=DictCursor) as cursor:

        cursor.execute('''select gr.profile_name
                        from "Locations" as l
                        join "LessonRows" as lr on lr.room_id = l.object_id
                        join "Groups" as gr on lr.group_id = gr.object_id
                        where
                        lr.day_of_the_week = %s
                        and
                        l.num_of_class = %s ''', ("пятница", 422))
        records = cursor.fetchall()
        print(*records, sep='')
cursor.close()
conn.close()
