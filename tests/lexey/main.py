from services.db_source_factory import DBFactory
from config import Configuration
from data_model.group import Group
from data_model.student import Student, StudentsForGroups
from data_model.lesson import Lesson
from datetime import date
import random, functions


cfg = Configuration()
dbf = DBFactory().set_db_source(host=cfg.get_configuration()["schedule_database"]["host"],
                           password=cfg.get_configuration()["schedule_database"]["password"],
                           user=cfg.get_configuration()["schedule_database"]["user"],
                           options=cfg.get_configuration()["schedule_database"]["options"])

source = dbf.get_db_source()

group = Group(source, 0, "Б", 11, "математика")
group.save()

alex = Student(source, "Алексей", 111111)
alex.save()
alex.append_group(group)

vasya = Student(source, "Василий", 121212)
vasya.save()
vasya.append_group(group)


subjects = functions.parse_subject(source, source.get_all("Subjects"))

teachers = functions.parse_teacher(source, source.get_all("Teachers"))

monday_pairs = int(input("Количество пар в понедельник:"))
thursday_pairs = int(input("Количество пар в четверг:"))
friday_pairs = int(input("Количество пар в пятницу:"))

functions.create_random_day(source, group, subjects, teachers, 5, monday_pairs)
functions.create_random_day(source, group, subjects, teachers, 8, thursday_pairs)
functions.create_random_day(source, group, subjects, teachers, 9, friday_pairs)

functions.get_data(source, group)

