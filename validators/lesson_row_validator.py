class LessonRowValidate:

    def __init__(self, request: dict, method: str):
        self.request = request
        self.method = method

    def validate(self):
        try:
            if self.method == 'POST':
                if set(self.request.keys()) == {'start_time', 'end_time', 'group_id', 'room_id',
                                                'timetable_id', 'day_of_the_week'}:
                    for key in self.request.keys():
                        if type(self.request[key]) != int:
                            raise ValueError
            if self.method == 'POST':
                if set(self.request.keys()) == {'start_time', 'end_time', 'group_id', 'room_id',
                                                'timetable_id', 'day_of_the_week', 'object_id'}:
                    for key in self.request.keys():
                        if type(self.request[key]) != int:
                            raise ValueError
        except ValueError:
            return '', 400