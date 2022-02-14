select DISTINCT
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
lsr.subject_id = sb.object_id