from adapters.db_source import DBSource

a = {"timetable_id": 49, 'start_time': '2022-05-01', 'stop_time': '2022-05-09'}
db = DBSource(user='schedule_app', password='VYRL!9XEB3yXQs4aPz_Q', host='postgresql.aakapustin.ru')
print(db.insert('NoLearningPeriods', a))

