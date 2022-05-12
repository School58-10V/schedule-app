class LessonRowValidate:

    def __init__(self, request: dict, method: str):
        self.request = request
        self.method = method

    def validate(self):

        if self.method == 'POST':
            if {'start_time', 'end_time', 'group_id', 'room_id', 'timetable_id', 'day_of_the_week'} \
                    in set(self.request.keys()):
                for key in self.request.keys():
                    if key not in {'start_time', 'end_time', 'group_id', 'room_id',
                                   'timetable_id', 'day_of_the_week', 'teachers'}:
                        raise ValueError
                    if key != 'teachers':
                        if type(self.request[key]) != int:
                            raise ValueError
                    if key == 'teacher':
                        if type(self.request[key]) != list:
                            raise ValueError
                        for i in self.request[key]:
                            if type(i) != int:
                                raise ValueError
            else:
                raise ValueError

        if self.method == 'PUT':
            if {'start_time', 'end_time', 'group_id', 'room_id', 'timetable_id',
                'day_of_the_week', 'object_id'} \
                    in set(self.request.keys()):
                for key in self.request.keys():
                    if key not in {'start_time', 'end_time', 'group_id', 'room_id',
                                   'timetable_id', 'day_of_the_week', 'teachers', 'object_id'}:
                        raise ValueError
                    if key != 'teachers':
                        if type(self.request[key]) != int:
                            raise ValueError
                    if key == 'teacher':
                        if type(self.request[key]) != list:
                            raise ValueError
                        for i in self.request[key]:
                            if type(i) != int:
                                raise ValueError
            else:
                raise ValueError