import validators.abstract_validator


class GroupValidator(validators.abstract_validator.AbstractValidator):
    def __init__(self):
        required_keys = {'teacher_id', 'class_letter', 'grade', 'profile_name'}
        allowed_keys = {'teacher_id', 'class_letter', 'grade', 'profile_name'}

        keys_types = {
            'teacher_id': int, 'grade': int, 'class_letter': str, 'profile_name': str
        }

        super(GroupValidator, self).__init__(required_keys, allowed_keys, keys_types)

    @staticmethod
    def get_name():
        return "group"
