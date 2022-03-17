from interfaces.student_interface import StudentInterface
from adapters.db_source import DBSource

a = StudentInterface(db_source=DBSource(host="postgresql.aakapustin.ru", password="VYRL!9XEB3yXQs4aPz_Q", user="schedule_app"), student_id=10)
a.main_loop()
