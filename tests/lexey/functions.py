import random
from datetime import date
from data_model.lesson import Lesson
from data_model.subject import Subject
from data_model.teacher import Teacher

def get_random_student(students):
    return students.get(random.randrange(0, len(students)))


def get_random_teachers(teachers):
    return teachers.get(random.randrange(0, len(teachers)))


def get_random_subject(subjects):
    return subjects.get(random.randrange(0, len(subjects)))


def create_random_lesson(source, group, subjects, teachers, day, start_time, end_time):
    Lesson(source, start_time, end_time, date(2022, 9, day), group_id=group.get_main_id(),
           subject_id=get_random_subject(subjects),
           teacher_id=get_random_teachers(teachers), notes="").save()


def create_random_day(source, group, subjects, teachers, day, pair_amount):
    start_time = 0
    end_time = 45
    for i in range(pair_amount * 2):
        create_random_lesson(source, group, subjects, teachers, day, start_time, end_time)
        if i % 2 == 0:
            breaktime = 10
        if i % 2 != 0:
            breaktime = 15
        start_time += 45 + breaktime
        end_time += 45 + breaktime

def parse_subject(source, data):
    return Subject(source, data.get("subject_name"), data.get("object_id"))

def parse_subjects(source, data):
    results = []
    for i in data:
        results.append(parse_subject(source, i))
    return results


def parse_teacher(source, data):
    return Teacher(source, data.get("fio"), data.get("object_id"), data.get("office_id"), data.get("bio"), data.get("contacts"))

def parse_teachers(source, data):
    results = []
    for i in data:
        results.append(parse_teacher(source, i))
    return results


def get_data(source, group):
    print(source.get_by_query(source, collection_name="Students", query={"bio": "пельмень"}))
    print(source.get_by_query(source, collection_name="Group", query={"profile_name": "математика"}))
    print(source.get_by_query(source, collection_name="Lesson", query={"group_id": group.get_main_id()}))
