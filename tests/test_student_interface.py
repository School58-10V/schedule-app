from adapters.db_source import DBSource
from interfaces.student_interface import StudentInterface


db = DBSource(dbname='schedule_app', user='schedule_app',
password='VYRL!9XEB3yXQs4aPz_Q', host='postgresql.aakapustin.ru')
a = StudentInterface(db, 1234)

a.main_loop()
