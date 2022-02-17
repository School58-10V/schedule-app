import psycopg2


conn = psycopg2.connect(
    dbname='schedule_app', user='',
    password='', host='postgresql.aakapustin.ru'
)
cursor = conn.cursor()

requests = [
    """
-- #2
select distinct
subj.name
from

"Students" as st
join "StudentsForGroups" as sfg on st.object_id = sfg.student_id
join "Groups" as g on sfg.group_id = g.object_id
join "LessonRows" as lr on lr.group_id = g.object_id
join "Subjects" as subj on subj.object_id = lr.subject_id
where
st.full_name = 'Фомин Влад Андреевич'
""",
    """
    select COUNT(subj.name) from
"Subjects" as subj
join "LessonRows" as lr on lr.subject_id = subj.object_id
join "TeachersForLessonRows" as tflr on lr.object_id = tflr.lesson_row_id
join "Teachers" as t on t.object_id = tflr.teacher_id

where
t.fio = 'Антон Антонович Антонов'
and
lr.day_of_the_week = 'пятница'
and
lr.start_time > 1000
""",
    """
select g.class_letter from
"Groups" as g
join "LessonRows" as lr on lr.group_id = g.object_id
join "Locations" as l on lr.room_id = l.object_id
where
lr.day_of_the_week = 'пятница'
and
l.object_id = 0
""",
    """
-- #5
select distinct
st.full_name
from
"Subjects" as subj
join "LessonRows" as lr on lr.subject_id = subj.object_id
join "StudentsForGroups" as sfg on sfg.group_id = lr.group_id
join "Students" as st on st.object_id = sfg.student_id

where
subj.name = 'Physics'"""
]

results = []
for i in range(len(requests)):
    cursor.execute(requests[i])
    data = cursor.fetchall()
    print(f'Результат {i + 1} запроса:')

    if len(data) == 0:
        print('*Пусто*')
    for j in range(len(data)):
        print(f'{j + 1 } результат: {", ".join([str(_) for _ in data[j]])}')
    print()

cursor.close()
conn.close()

