class LessonValidate:

    def __init__(self, request: dict, method: str):
        self.request = request
        self.method = method

    def validate(self):
        try:

            if self.method == 'POST':
                if set(self.request.keys()) == {"start_time", "end_time", "notes", "state", "teacher_id", "group_id",
                                                "subject_id", "date"}:
                    for key in self.request.keys():
                        if key == 'start_time' or key == 'end_time' or key == 'teacher_id' or \
                                key == 'group_id' or key == 'subject_id' or key == 'date':
                            if type(self.request[key]) != int:
                                raise ValueError
                        if key == 'state':
                            if type(self.request[key]) != bool:
                                raise ValueError
                        if key == 'notes':
                            if type(self.request[key]) != str:
                                raise ValueError
                else:
                    raise ValueError

            if self.method == 'PUT':
                if set(self.request.keys()) == {"start_time", "end_time", "notes", "state", "teacher_id", "group_id",
                                                "subject_id", "date", "object_id"}:
                    for key in self.request.keys():
                        if key == 'start_time' or key == 'end_time' or key == 'teacher_id' or \
                                key == 'group_id' or key == 'subject_id' or key == 'date' or key == 'object_id':
                            if type(self.request[key]) != int:
                                raise ValueError
                        if key == 'state':
                            if type(self.request[key]) != bool:
                                raise ValueError
                        if key == 'notes':
                            if type(self.request[key]) != str:
                                raise ValueError
                else:
                    raise ValueError

        except ValueError:
            return '', 400