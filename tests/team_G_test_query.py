import psycopg2


day = 'пятница'
teacher = 'Антон Антонович Антонов'
time = 1000

student = 'Бугаенко Оля Алексеевна'
year = 2020

conn = psycopg2.connect(dbname='schedule_app', user='kuranova',
                        password='s9iz.4c-yC-LREFf_63_', host='postgresql.aakapustin.ru')
cursor = conn.cursor()
# Запрос 2
cursor.execute(f'''select count (distinct lr.object_id) from
                 "Teachers" as tc
                 join "TeachersForLessonRows" as tlr on tlr.teacher_id = tc.object_id
                 join "LessonRows" as lr on lr.object_id = tlr.lesson_row_id
                 where
                 lr.day_of_the_week = '{day}'
                 and
                 tc.fio = '{teacher}'
                 and
                 lr.start_time > {time}''')
records = cursor.fetchall()

# Запрос 1
cursor.execute(f'''select distinct sb.name from
                 "Students" as st
                 join "StudentsForGroups" as stg on stg.student_id = st.object_id
                 join "LessonRows" as lr on lr.group_id = stg.group_id
                 join "TimeTables" as tb on tb.object_id = lr.timetable_id
                 join "Subjects" as sb on lr.subject_id = sb.object_id
                 where
                 st.full_name = '{student}'
                 and
                 tb.time_table_year = {year}
                 ''')
records2 = cursor.fetchall()

# Запрос 3
cursor.execute('''select DISTINCT
                  st.full_name, st.object_id,
                  sb.name
                  from
                  "Students" as st,
                  "StudentsForGroups" as stfg,
                  "Groups" as gr,
                  "LessonRows" as lsr,
                  "Teachers" as tch,
                  "Subjects" as sb
                  where
                  sb.name = 'English'
                  and
                  st.object_id = stfg.student_id
                  and
                  stfg.group_id = gr.object_id
                  and
                  gr.object_id = lsr.group_id
                  and
                  lsr.subject_id = sb.object_id''')
records3 = cursor.fetchall()

cursor.close()
conn.close()
try:
    records = records[0]
    records2 = records2[0]
except IndexError:
    pass
# Печатаем запросы.
# Запрос 1
print(f"Количество уроков, которое осталость вести "
      f"учителю с именем {teacher} в день"
      f" недели {day} после {time}:", *records)
print()
# Запрос 2
print(f"Предметы, которые изучает ученик {student} в {year} году:", *records2)
print()
# Запрос 3
print(*records3)
print()
