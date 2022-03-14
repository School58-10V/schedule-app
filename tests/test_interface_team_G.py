from interfaces.student_interface import StudentInterface
from adapters.db_source import DBSource

db_source = DBSource(dbname='schedule_app', user='giglionda',
                     password='fu9FvALTYwcyvwr!JeHc', host='postgresql.aakapustin.ru')
st_int = StudentInterface(db_source, 123)
st_int.main_loop()

