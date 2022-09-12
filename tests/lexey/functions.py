import random
from data_model.lesson_row import LessonRow
from data_model.subject import Subject
from data_model.teacher import Teacher
from data_model.student import Student

def get_random_student(students):
    return students[random.randrange(0, len(students))]


def get_random_teachers(teachers):
    return teachers[random.randrange(0, len(teachers))]


def get_random_subject(subjects):
    return subjects[random.randrange(0, len(subjects))]

def create_random_lesson_row(source, group, subject, teacher, day, start_time, end_time):
    return LessonRow(source, day, start_time=start_time, end_time=end_time, group_id=group.get_main_id(), subject_id=subject,
              room_id=teacher.get_office_id(), timetable_id=41).save().append_teacher(teacher)


def create_random_day(source, group, subjects, teachers, day, pair_amount):
    start_time = 900
    end_time = 945
    for i in range(pair_amount * 2):
        create_random_lesson_row(source, group, get_random_subject(subjects), get_random_teachers(teachers), day, start_time, end_time)
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
    dates = list(range(0, 6))
    result = []
    for i in range(dates_amount):
        result.append(dates.pop(random.randrange(0, len(dates))))
    return result

def process_students(source, students, group):
    people = {}
    req_names = {"Алексей": "2005-06-23", "Василий": "2005-06-21", "Иван": "2005-04-19"}
    for student in students:
        if student.get_name() in req_names and student.get_name() not in people:
            people[student.get_name()] = student
    for name in req_names:
        if name not in people:
            people[name] = Student(source, name, req_names[name], bio="пельмень").save().append_group(group)
    return list(people.values())