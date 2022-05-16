class NoLearningPeriodValidator:

    def validate(self, request: dict, method: str):

        if method == 'POST':
            if set(request.keys()) != {'timetable_id', 'start_time', 'stop_time'}:
                raise ValueError
        if method == 'PUT':
            if set(request.keys()) != {'timetable_id', 'start_time', 'stop_time', 'object_id'}:
                raise ValueError

        for key in request.keys():
            if type(request[key]) != int:
                raise ValueError
