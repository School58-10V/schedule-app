class LessonValidate:

    def __init__(self, request: dict, method: str):
        self.request = request
        self.method = method

    def validate(self):
        try:
            if self.method == 'POST':
                if set(self.request.keys()) == {"start_time", "end_time", "notes", "state", "teacher_id", "group_id",
                                                "subject_id", "date"}:
                    if type(self.request["start_time"]) != int:
                        raise ValueError
                    if type(self.request["end_time"]) != int:
                        raise ValueError
                    if type(self.request["notes"]) != str:
                        raise ValueError
                    if type(self.request["state"]) != bool:
                        raise ValueError
                    if type(self.request["teacher_id"]) != int:
                        raise ValueError
                    if type(self.request["group_id"]) != int:
                        raise ValueError
                    if type(self.request["subject_id"]) != int:
                        raise ValueError
                    if type(self.request["date"]) != int:
                        raise ValueError

            if self.method == 'PUT':
                if set(self.request.keys()) == {"start_time", "end_time", "notes", "state", "teacher_id", "group_id",
                                                "subject_id", "date", "object_id"}:
                    if type(self.request["start_time"]) != int:
                        raise ValueError
                    if type(self.request["end_time"]) != int:
                        raise ValueError
                    if type(self.request["notes"]) != str:
                        raise ValueError
                    if type(self.request["state"]) != bool:
                        raise ValueError
                    if type(self.request["teacher_id"]) != int:
                        raise ValueError
                    if type(self.request["group_id"]) != int:
                        raise ValueError
                    if type(self.request["subject_id"]) != int:
                        raise ValueError
                    if type(self.request["date"]) != int:
                        raise ValueError
                    if type(self.request["object_id"]) != int:
                        raise ValueError

        except ValueError:
            return '', 400