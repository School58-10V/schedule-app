class LessonValidator:

    def validate(self, request: dict, method: str):

        if method == 'POST':
            if set(request.keys()) == {"start_time", "end_time", "notes", "state", "teacher_id", "group_id",
                                       "subject_id", "date"}:
                for key in request.keys():
                    if key == 'start_time' or key == 'end_time' or key == 'teacher_id' or \
                            key == 'group_id' or key == 'subject_id' or key == 'date':
                        if type(request[key]) != int:
                            raise ValueError
                    if key == 'state':
                        if type(request[key]) != bool:
                            raise ValueError
                    if key == 'notes':
                        if type(request[key]) != str:
                            raise ValueError
            else:
                raise ValueError

        if method == 'PUT':
            if set(request.keys()) == {"start_time", "end_time", "notes", "state", "teacher_id", "group_id",
                                       "subject_id", "date", "object_id"}:
                for key in request.keys():
                    if key == 'start_time' or key == 'end_time' or key == 'teacher_id' or \
                            key == 'group_id' or key == 'subject_id' or key == 'date' or key == 'object_id':
                        if type(request[key]) != int:
                            raise ValueError
                    if key == 'state':
                        if type(request[key]) != bool:
                            raise ValueError
                    if key == 'notes':
                        if type(request[key]) != str:
                            raise ValueError
            else:
                raise ValueError
