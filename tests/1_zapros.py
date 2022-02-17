import psycopg2
from psycopg2.extras import DictCursor

conn = psycopg2.connect(dbname='schedule_app', user='giglionda',
                        password='fu9FvALTYwcyvwr!JeHc', host='postgresql.aakapustin.ru')
cursor = conn.cursor(cursor_factory=DictCursor)

dct = {1: """
select DISTINCT st.full_name from "Teachers" as tch
join "TeachersForLessonRows" as tflr on tch.object_id = tflr.teacher_id
join "LessonRows" as lr on lr.object_id = tflr.lesson_row_id
join "Groups" as gr on lr.group_id = gr.object_id
join "StudentsForGroups" as sfg on sfg.group_id = gr.object_id
join "Students" as st on st.object_id = sfg.student_id
where
tch.fio = 'Антон Антонович Антонов'
and
lr.day_of_the_week = 'пятница'
""",
    2: """
select distinct sbj.name from "Students" as st
join "StudentsForGroups" as sfg on st.object_id = sfg.student_id
join "Groups" as gr on sfg.group_id = gr.object_id
join "LessonRows" as lr on lr.group_id = gr.object_id
join "TimeTables" as tt on lr.timetable_id = tt.object_id
join "Subjects" as sbj on sbj.object_id = lr.subject_id
where
st.full_name = 'Фомин Влад Андреевич'
and
tt.time_table_year = 2020
""",
    3: """
select count (lr.object_id) from
"Teachers" as tch
join "TeachersForLessonRows" as tflr on tch.object_id = tflr.teacher_id
join "LessonRows" as lr on lr.object_id = tflr.lesson_row_id
where
tch.fio = 'Антон Антонович Антонов'
and
lr.day_of_the_week = 'пятница'
and
lr.start_time > 1100
""", 4: """
select DISTINCT gr from
"Locations" as loc
join "LessonRows" as lr on lr.room_id = loc.object_id
join "Groups" as gr on lr.group_id = gr.object_id
where
loc.num_of_class = 422
and
lr.day_of_the_week = 'пятница'
""",
    5: """
select DISTINCT st.full_name from
"Subjects" as sb
join "LessonRows" as lr on lr.subject_id = sb.object_id
join "Groups" as gr on lr.group_id = gr.object_id
join "StudentsForGroups" as sfg on sfg.group_id = gr.object_id
join "Students" as st on st.object_id = sfg.student_id
where
sb.name = 'Mathematics'
"""}
print('Выберите цифру: 1. запрос, который показывает, у каких студентов преподаватель с известным именем ведет уроки в известный день',
      '2. Написать запрос, который показывает все предметы, которые изучает известный ученик в известном году ',
      '3. Написать запрос, который показывает количество (только) уроков, оставшихся сегодня (в известный день) у известного учителя ',
      '4. Написать запрос, который показывает, какие группы будут пользоваться известным кабинетом в известный день ',
      '5. Написать запрос, который показывает, какие ученики проходят обучение по известному предмету (у любого учителя)', sep="\n", end='\n')
number = input()
while str(number) not in ['1', '2', '3', '4', '5']:
    number = input('Неверный ввод данных, попробуйте еще раз.\n')
cursor.execute(dct[int(number)])
records = cursor.fetchall()
print(records)
...
cursor.close()
conn.close()