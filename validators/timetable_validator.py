import validators.abstract_validator


class TimetableValidator(validators.abstract_validator.AbstractValidator):
    def __init__(self):
        required_keys = {}
        allowed_keys = {'time_table_year', 'version'}

        keys_types = {'time_table_year': int, 'version': int}

        super(TimetableValidator, self).__init__(required_keys, allowed_keys, keys_types)
