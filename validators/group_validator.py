class GroupValidator:

    def validate(self, request: dict, method: str):

        required_keys = {'teacher_id', 'class_letter', 'grade', 'profile_name'}
        allowed_keys = {'teacher_id', 'class_letter', 'grade', 'profile_name'}

        if method == 'PUT':
            required_keys.add('object_id')
            allowed_keys.add('object_id')

        for key in required_keys:
            if key not in request.keys():
                raise ValueError

        for key in request.keys():
            if key not in allowed_keys:
                raise ValueError
            if key == 'teacher_id' or key == 'grade':
                if type(request[key]) != int:
                    raise ValueError
            if key == 'class_letter' or key == 'profile_name':
                if type(request[key]) != str:
                    raise ValueError
