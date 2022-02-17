from adapters.db_source import DBSource

a = {"day_of_the_week": "Пятница", "group_id": 671, "subject_id": 108425849, "room_id": 1, "start_time": 1230, "end_time": 1315, "timetable_id": 11}
b = {"full_name": "Иван Иванович", "date_of_birth": "8-5-21", "contacts": "2947", "bio": "аркада"}
db = DBSource(user='schedule_app', password='VYRL!9XEB3yXQs4aPz_Q', host='postgresql.aakapustin.ru')
db.insert('Student', b)