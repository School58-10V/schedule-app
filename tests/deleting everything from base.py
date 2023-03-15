import psycopg2
from psycopg2 import errorcodes


for object_id in range(52, 59):
    conn = psycopg2.connect(host="postgresql.aakapustin.ru",
                 password="VYRL!9XEB3yXQs4aPz_Q",
                 user="schedule_app")
    cursor = conn.cursor()
    try:
        request = f'DELETE FROM "Students" WHERE object_id = {object_id}'
        cursor.execute(request)
        conn.commit()
        print('Удалил', object_id)
    except psycopg2.Error as e:
        print(f"Неизвестная ошибка . Код ошибки: {errorcodes.lookup(e.pgcode)}")
    finally:
        cursor.close()
        conn.close()
