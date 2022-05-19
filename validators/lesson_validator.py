class LessonValidator:

    def validate(self, request: dict, method: str):

        required_keys = {'start_time', 'end_time', 'notes', 'state', 'teacher_id', 'group_id', 'subject_id', 'date'}
        allowed_keys = {'start_time', 'end_time', 'notes', 'state', 'teacher_id', 'group_id', 'subject_id', 'date'}

        if method == 'PUT':
            required_keys.add('object_id')
            allowed_keys.add('object_id')

        for key in required_keys:
            if key not in request.keys():
                raise ValueError

        for key in request.keys():
            if key not in allowed_keys:
                raise ValueError
            if key == 'start_time' or key == 'end_time' or key == 'teacher_id' or \
                    key == 'group_id' or key == 'subject_id':
                if type(request[key]) != int:
                    raise ValueError
            if key == 'state':
                if type(request[key]) != bool:
                    raise ValueError
            if key == 'notes' or key == 'date':
                if type(request[key]) != str:
                    raise ValueError
