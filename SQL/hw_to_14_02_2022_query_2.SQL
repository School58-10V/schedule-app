#Написать запрос, который показывает количество (только) уроков, оставшихся сегодня (в известный день) у известного учителя
select count (distinct lr.object_id) from
"Teachers" as tc
join "TeachersForLessonRows" as tlr on tlr.teacher_id = tc.object_id
join "LessonRows" as lr on lr.object_id = tlr.lesson_row_id
where
lr.day_of_the_week = 'пятница'
and
tc.fio = 'Антон Антонович Антонов'
and
lr.start_time > 2000
