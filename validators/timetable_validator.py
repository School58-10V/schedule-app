import validators.abstract_validator


class TimeTableValidator(validators.abstract_validator.AbstractValidator):

    def validate(self, request: dict, method: str):

        required_keys = {'time_table_year'}
        allowed_keys = {'time_table_year'}

        if method == 'PUT':
            required_keys.add('object_id')
            allowed_keys.add('object_id')

        for key in required_keys:
            if key not in request.keys():
                raise ValueError

        for key in request.keys():
            if key not in allowed_keys:
                raise ValueError
            if key == 'time_table_year':
                if type(request[key]) != int:
                    raise ValueError

    @staticmethod
    def get_name():
        return "timetable"