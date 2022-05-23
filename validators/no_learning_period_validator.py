import validators.abstract_validator


class NoLearningPeriodValidator(validators.abstract_validator.AbstractValidator):
    def __init__(self):
        required_keys = {'timetable_id', 'start_time', 'stop_time'}
        allowed_keys = {'timetable_id', 'start_time', 'stop_time'}

        keys_types = {'timetable_id': int, 'start_time': int, 'stop_time': int}

        super(NoLearningPeriodValidator, self).__init__(required_keys, allowed_keys, keys_types)

    @staticmethod
    def get_name():
        return "nolearningperiod"
