import validators.abstract_validator


class TeacherValidator(validators.abstract_validator.AbstractValidator):

    def validate(self, request: dict, method: str):

        required_keys = {'fio'}
        allowed_keys = {'fio', 'bio', 'contacts', 'office_id', 'subject_id', 'lesson_row_id'}

        if method == 'PUT':
            required_keys.add('object_id')
            allowed_keys.add('object_id')

        for key in required_keys:
            if key not in request.keys():
                raise ValueError

        for key in request.keys():
            if key not in allowed_keys:
                raise ValueError
            if key == 'fio' or key == 'bio' or 'contacts':
                if type(request[key]) != str:
                    raise ValueError
            if key == 'office_id':
                if type(request[key]) != int:
                    raise ValueError
            if key == 'subject_id' or key == 'lesson_row_id':
                for i in request[key]:
                    if type(i) != int:
                        raise ValueError

    @staticmethod
    def get_name():
        return "teacher"