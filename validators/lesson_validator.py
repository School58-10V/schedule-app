import validators.abstract_validator


class LessonValidator(validators.abstract_validator.AbstractValidator):
    def __init__(self):
        required_keys = {'start_time', 'end_time', 'notes', 'state', 'teacher_id', 'group_id', 'subject_id', 'date'}
        allowed_keys = {'start_time', 'end_time', 'notes', 'state', 'teacher_id', 'group_id', 'subject_id', 'date'}

        keys_types = {
            'start_time': int, 'end_time': int, 'notes': str, 'state': bool,
            'teacher_id': int, 'group_id': int, 'subject_id': int, 'date': str
        }

        super(LessonValidator, self).__init__(required_keys, allowed_keys, keys_types)

