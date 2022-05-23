import validators.abstract_validator


class LessonRowValidator(validators.abstract_validator.AbstractValidator):
    def __init__(self):
        required_keys = {'start_time', 'end_time', 'group_id', 'room_id', 'timetable_id', 'day_of_the_week'}
        allowed_keys = {'start_time', 'end_time', 'group_id', 'room_id', 'timetable_id', 'day_of_the_week', 'teachers'}
        keys_types = {
            'teacher': 'list[int]',  # <- эту конструкцию можно поменять
            'start_time': int, 'end_time': int, 'group_id': int, 'room_id': int,
            'timetable_id': int, 'day_of_the_week': int
        }

        super(LessonRowValidator, self).__init__(required_keys, allowed_keys, keys_types)

    @staticmethod
    def get_name():
        return "lessonrow"
