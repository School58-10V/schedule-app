import validators.abstract_validator


class TeacherValidator(validators.abstract_validator.AbstractValidator):
    def __init__(self):
        required_keys = {'fio'}
        allowed_keys = {'fio', 'bio', 'contacts', 'office_id', 'subject_id', 'lesson_row_id'}

        keys_types = {'fio': str, 'bio': str, 'contacts': str, 'office_id': int,
                      'subject_id': int, 'lesson_row_id': 'list[int]'}

        super(TeacherValidator, self).__init__(required_keys, allowed_keys, keys_types)
