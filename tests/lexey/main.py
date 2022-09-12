from services.db_source_factory import DBFactory
from config import Configuration
from data_model.group import Group
from data_model.student import Student
from tests.lexey import functions

cfg = Configuration("../../config.json")
dbf = DBFactory()
dbf.set_db_source(host=cfg.get_configuration()["schedule_database"]["host"],
                                password=cfg.get_configuration()["schedule_database"]["password"],
                                user=cfg.get_configuration()["schedule_database"]["user"],
                                options=cfg.get_configuration()["schedule_database"]["options"])

source = dbf.get_db_source()

group = Group(source, 4, "Б", 11, "математика")
group.save()

alex = Student(source, "Алексей", "2005-06-23", bio="пельмень")
alex.save()
alex.append_group(group)

vasya = Student(source, "Василий", "2005-06-21", bio="пельмень")
vasya.save()
vasya.append_group(group)

vanya = Student(source, "Иван", "2005-04-19", bio="пельмень")
vanya.save()
vanya.append_group(group)

subjects = functions.parse_subjects(source, source.get_all("Subjects"))

teachers = functions.parse_teachers(source, source.get_all("Teachers"))

monday_pairs = int(input("Количество пар в понедельник:"))
thursday_pairs = int(input("Количество пар в четверг:"))
friday_pairs = int(input("Количество пар в пятницу:"))

dates = functions.get_rand_dates()

functions.create_random_day(source, group, subjects, teachers, dates[0], monday_pairs)
functions.create_random_day(source, group, subjects, teachers, dates[1], thursday_pairs)
functions.create_random_day(source, group, subjects, teachers, dates[2], friday_pairs)

functions.get_data(source, group)
