class LessonRowValidator:

    def validate(self, request: dict, method: str):

        required_keys = {'start_time', 'end_time', 'group_id', 'room_id', 'timetable_id', 'day_of_the_week'}
        allowed_keys = {'start_time', 'end_time', 'group_id', 'room_id', 'timetable_id', 'day_of_the_week', 'teachers', 'subject_id'}

        if method == 'PUT':
            required_keys.add('object_id')
            allowed_keys.add('object_id')

        for key in required_keys:
            if key not in request.keys():
                raise ValueError

        for key in request.keys():
            if key not in allowed_keys:
                raise ValueError
            if key != 'teachers':
                if type(request[key]) != int:
                    raise ValueError
            if key == 'teacher':
                if type(request[key]) != list:
                    raise ValueError
                for i in request[key]:
                    if type(i) != int:
                        raise ValueError