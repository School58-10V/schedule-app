from adapters.db_source import DBSource
from interfaces.student_interface import StudentInterface

a = StudentInterface(DBSource(dbname='schedule_app', user='giglionda',
                              password='fu9FvALTYwcyvwr!JeHc', host='postgresql.aakapustin.ru'), 1)
a.main_loop()
