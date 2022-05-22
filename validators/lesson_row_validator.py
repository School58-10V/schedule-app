class LessonRowValidator:
    def validate(self, request: dict, method: str):
        required_keys = {'start_time', 'end_time', 'subject_id', 'group_id', 'room_id', 'timetable_id',
                         'day_of_the_week'}
        allowed_keys = {'start_time', 'end_time', 'group_id', 'subject_id', 'room_id', 'timetable_id',
                        'day_of_the_week', 'teachers'}

        for key in required_keys:
            if key not in request.keys():
                print(request.keys())
                print(allowed_keys)
                raise ValueError

        for key in request.keys():
            if key not in allowed_keys:
                print(request.keys())
                print(allowed_keys)
                raise ValueError
            if key != 'teachers':
                if type(request[key]) != int:
                    print(request.keys())
                    print(allowed_keys)
                    raise ValueError
            if key == 'teacher':
                if type(request[key]) != list:
                    print(request.keys())
                    print(allowed_keys)
                    raise ValueError
                for i in request[key]:
                    if type(i) != int:
                        print(request.keys())
                        print(allowed_keys)
                        raise ValueError
