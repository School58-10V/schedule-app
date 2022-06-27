import validators.abstract_validator


class TimetableValidator(validators.abstract_validator.AbstractValidator):
    def __init__(self):
        required_keys = {'time_table_year'}
        allowed_keys = {'time_table_year'}

        keys_types = {'time_table_year': int}

        super(TimetableValidator, self).__init__(required_keys, allowed_keys, keys_types)
