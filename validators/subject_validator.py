import validators.abstract_validator


class SubjectValidator(validators.abstract_validator.AbstractValidator):
    def __init__(self):
        required_keys = {'subject_name'}
        allowed_keys = {'subject_name', 'teachers'}

        keys_types = {'subject_name': str, 'teachers': 'list[int]'}

        super(SubjectValidator, self).__init__(required_keys, allowed_keys, keys_types)