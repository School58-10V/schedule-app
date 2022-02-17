import psycopg2
from psycopg2.extras import DictCursor

conn = psycopg2.connect(dbname='schedule_app', user='giglionda',
                        password='fu9FvALTYwcyvwr!JeHc', host='postgresql.aakapustin.ru')
cursor = conn.cursor(cursor_factory=DictCursor)
collection_name = 'Teachers'
values = collection_name[:-1].__dict__.keys()
cursor.execute(f"""
INSERT INTO {collection_name}
                          (id, name, email, joining_date, salary)
                          VALUES
                          (1, 'Oleg', 'oleg04@gmail.com', '2020-11-29', 8100)
""")
records = cursor.fetchall()
print(records)
...
cursor.close()
conn.close()