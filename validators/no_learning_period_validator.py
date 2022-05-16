class NoLearningPeriodValidate:

    def __init__(self, request: dict, method: str):
        self.request = request
        self.method = method

    def validate(self):

            if self.method == 'POST':
                if set(self.request.keys()) != {'timetable_id', 'start_time', 'stop_time'}:
                    raise ValueError
            if self.method == 'PUT':
                if set(self.request.keys()) != {'timetable_id', 'start_time', 'stop_time', 'object_id'}:
                    raise ValueError

            for key in self.request.keys():
                if type(self.request[key]) != int:
                    raise ValueError

