from adapters.db_source import DBSource

a = {"day_of_the_week": "Среда", "group_id": 6712, "subject_id": 108425849, "room_id": 1, "start_time": 1530, "end_time": 1615, "timetable_id": 11}
b = {"full_name": "Иваноооооов Иванович Ангельский", "date_of_birth": "8-5-24", "contacts": "2947123123", "bio": "аркада"}
db = DBSource(user='schedule_app', password='VYRL!9XEB3yXQs4aPz_Q', host='postgresql.aakapustin.ru')
print(db.insert('Students', b))
print(db.insert('Students', b))

