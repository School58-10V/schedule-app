import random
from datetime import date
from data_model.lesson import Lesson
from data_model.subject import Subject
from data_model.teacher import Teacher

def get_random_student(students):
    return students[random.randrange(0, len(students))]


def get_random_teachers(teachers):
    return teachers[random.randrange(0, len(teachers))]


def get_random_subject(subjects):
    return subjects[random.randrange(0, len(subjects))]


def create_random_lesson(source, group, subjects, teachers, day, start_time, end_time):
    Lesson(source, start_time, end_time, date(2022, 9, day), group_id=group.get_main_id(),
           subject_id=get_random_subject(subjects).get_main_id(),
           teacher_id=get_random_teachers(teachers).get_main_id(), notes="test").save()


def create_random_day(source, group, subjects, teachers, day, pair_amount):
    start_time = 900
    end_time = 945
    for i in range(pair_amount * 2):
        create_random_lesson(source, group, subjects, teachers, day, start_time, end_time)
        if i % 2 == 0:
            breaktime = 10
        if i % 2 != 0:
            breaktime = 15
        start_time += 45 + breaktime
        end_time += 45 + breaktime

def parse_subject(source, data):
    return Subject(source, data["subject_name"], data["object_id"])

def parse_subjects(source, data):
    results = []
    for i in data:
        results.append(parse_subject(source, i))
    return results


def parse_teacher(source, data):
    return Teacher(source, data["fio"], data["object_id"], data["office_id"], data["bio"], data["contacts"])

def parse_teachers(source, data):
    results = []
    for i in data:
        results.append(parse_teacher(source, i))
    return results


def get_data(source, group):
    print(source.get_by_query(collection_name="Students", query={"bio": "пельмень"}))
    print(source.get_by_query(collection_name="Group", query={"profile_name": "математика"}))
    print(source.get_by_query(collection_name="Lesson", query={"group_id": group.get_main_id()}))

def get_rand_dates(dates_amount=3):
    dates = list(range(13, 17))
    result = []
    for i in range(dates_amount):
        result.append(dates.pop(random.randrange(0, len(dates))))
    return result