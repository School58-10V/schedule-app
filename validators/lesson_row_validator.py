class LessonRowValidator:

    def validate(self, request: dict, method: str):

        if method == 'POST':
            if {'start_time', 'end_time', 'group_id', 'room_id', 'timetable_id', 'day_of_the_week'} \
                    in set(request.keys()):
                for key in request.keys():
                    if key not in {'start_time', 'end_time', 'group_id', 'room_id',
                                   'timetable_id', 'day_of_the_week', 'teachers'}:
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
            else:
                raise ValueError

        if method == 'PUT':
            if {'start_time', 'end_time', 'group_id', 'room_id', 'timetable_id',
                'day_of_the_week', 'object_id'} \
                    in set(request.keys()):
                for key in request.keys():
                    if key not in {'start_time', 'end_time', 'group_id', 'room_id',
                                   'timetable_id', 'day_of_the_week', 'teachers', 'object_id'}:
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
            else:
                raise ValueError
