class NoLearningPeriodValidator:

    def validate(self, request: dict, method: str):

        required_keys = {'timetable_id', 'start_time', 'stop_time'}
        allowed_keys = {'timetable_id', 'start_time', 'stop_time'}

        if method == 'PUT':
            required_keys.add('object_id')
            allowed_keys.add('object_id')

        for key in required_keys:
            if key not in request.keys():
                raise ValueError

        for key in request.keys():
            if key not in allowed_keys:
                raise ValueError
            if key == 'start_time' or key == 'stop_time':
                if type(request[key]) != str:
                    raise ValueError
            if key == 'timetable_id':
                if type(request[key]) != int:
                    print(key)
                    raise ValueError

