import psycopg2
from psycopg2 import errorcodes
from psycopg2.extras import DictCursor


for object_id in range(50, 52):
    conn = psycopg2.connect(dbname='schedule_app', user='giglionda',
                            password='fu9FvALTYwcyvwr!JeHc', host='postgresql.aakapustin.ru')
    cursor = conn.cursor(cursor_factory=DictCursor)
    try:
        request = f'DELETE FROM "TimeTables" WHERE object_id = {object_id}'
        cursor.execute(request)
        conn.commit()
        print('Удалил', object_id)
        cursor.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"Неизвестная ошибка . Код ошибки: {errorcodes.lookup(e.pgcode)}")
        cursor.close()
        conn.close()
        continue