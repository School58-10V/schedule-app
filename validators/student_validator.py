import validators.abstract_validator


class StudentValidator(validators.abstract_validator.AbstractValidator):
    def __init__(self):
        required_keys = {'full_name', 'date_of_birth'}
        allowed_keys = {'full_name', 'date_of_birth', 'contacts', 'bio'}

        keys_types = {'full_name': str, 'date_of_birth': int, 'contacts': str, 'bio': str}

        super(StudentValidator, self).__init__(required_keys, allowed_keys, keys_types)
