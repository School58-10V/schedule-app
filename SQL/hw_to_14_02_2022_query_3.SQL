select DISTINCT
gr.object_id, gr.profile_name
from
"LessonRows" as lr,
"Groups" as gr
where
lr.day_of_the_week = 'пятница'
and
lr.room_id = 1
and
lr.group_id = gr.object_id