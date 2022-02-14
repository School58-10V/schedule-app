# Написать запрос, который показывает все предметы, которые изучает известный ученик в известном году

select distinct sb.name from
"Students" as st
join "StudentsForGroups" as stg on stg.student_id = st.object_id
join "LessonRows" as lr on lr.group_id = stg.group_id
join "TimeTables" as tb on tb.object_id = lr.timetable_id
join "Subjects" as sb on lr.subject_id = sb.object_id
where
st.full_name = 'Фомин Влад Андреевич'
and
tb.time_table_year = 2019
