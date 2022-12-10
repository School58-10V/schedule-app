from services.db_source_factory import DBFactory
from config import Configuration
from tests.lexey import functions

cfg = Configuration("../../config.json")
dbf = DBFactory()
dbf.set_db_source(host=cfg.get_configuration()["schedule_database"]["host"],
                                password=cfg.get_configuration()["schedule_database"]["password"],
                                user=cfg.get_configuration()["schedule_database"]["user"],
                                options=cfg.get_configuration()["schedule_database"]["options"])

source = dbf.get_db_source()

group = functions.parse_group(source, source.get_by_id("Groups", 55))
students = functions.process_students(source, functions.parse_students(source, source.get_all("Students")), group)
subjects = functions.parse_subjects(source, source.get_all("Subjects"))
teachers = functions.parse_teachers(source, source.get_all("Teachers"))

dates = functions.get_rand_dates()

for date in dates:
    functions.create_random_day(source, group, subjects, teachers, date, int(input(f"Количество пар в {date + 1} день недели: ")))

functions.get_data(source, group)
