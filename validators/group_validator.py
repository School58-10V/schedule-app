import validators.abstract_validator


class GroupValidator(validators.abstract_validator.AbstractValidator):
    def __init__(self):
        required_keys = {'teacher_id', 'class_letter', 'grade', 'profile_name'}
        allowed_keys = {'teacher_id', 'class_letter', 'grade', 'profile_name', 'students'}

        keys_types = {
            'teacher_id': int, 'class_letter': str, 'grade': int, 'profile_name': str, 'students': 'list[int]'
        }

        super(GroupValidator, self).__init__(required_keys, allowed_keys, keys_types)