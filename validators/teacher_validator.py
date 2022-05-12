class TeacherValidator:

    def __init__(self, request: dict, method: str):
        self.request = request
        self.method = method

    def validate(self):

        if self.method == 'POST':
            if 'fio' in self.request.keys():
                for key in self.request.keys():
                    if key not in {'fio', 'bio', 'contacts', 'office_id', 'subject_id', 'lesson_row_id'}:
                        raise ValueError
                    if key == 'fio' or key == 'bio' or 'contacts':
                        if type(self.request[key]) != str:
                            raise ValueError
                    if key == 'office_id':
                        if type(self.request[key]) != int:
                            raise ValueError
                    if key == 'subject_id' or key == 'lesson_row_id':
                        for i in self.request[key]:
                            if type(i) != int:
                                raise ValueError
            else:
                raise ValueError

        if self.method == 'PUT':
            if {'fio', 'object_id'} in set(self.request.keys()):
                for key in self.request.keys():
                    if key not in {'fio', 'bio', 'contacts', 'office_id', 'object_id', 'subject_id', 'lesson_row_id'}:
                        raise ValueError
                    if key == 'fio' or key == 'bio' or 'contacts':
                        if type(self.request[key]) != str:
                            raise ValueError
                    if key == 'office_id' or key == 'object_id':
                        if type(self.request[key]) != int:
                            raise ValueError
                    if key == 'subject_id' or key == 'lesson_row_id':
                        for i in self.request[key]:
                            if type(i) != int:
                                raise ValueError
            else:
                raise ValueError