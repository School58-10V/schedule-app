import validators.abstract_validator


class SubjectValidator(validators.abstract_validator.AbstractValidator):

    def validate(self, request: dict, method: str):

        required_keys = {'subject_name'}
        allowed_keys = {'subject_name', 'teachers'}

        if method == 'PUT':
            required_keys.add('object_id')
            allowed_keys.add('object_id')

        for key in required_keys:
            if key not in request.keys():
                raise ValueError

        for key in request.keys():
            if key not in allowed_keys:
                raise ValueError
            if key == 'subject_name':
                if type(request[key]) != str:
                    raise ValueError
            if key == 'teachers':
                if type(request[key]) != list:
                    raise ValueError
                for teacher_id in request[key]:
                    if type(teacher_id) != int:
                        raise ValueError

    @staticmethod
    def get_name():
        return "subject"