class TeacherValidator:

    def validate(self, request: dict, method: str):

        if method == 'POST':
            if 'fio' in request.keys():
                for key in request.keys():
                    if key not in {'fio', 'bio', 'contacts', 'office_id', 'subject_id', 'lesson_row_id'}:
                        raise ValueError
                    if key == 'fio' or key == 'bio' or 'contacts':
                        if type(request[key]) != str:
                            raise ValueError
                    if key == 'office_id':
                        if type(request[key]) != int:
                            raise ValueError
                    if key == 'subject_id' or key == 'lesson_row_id':
                        for i in request[key]:
                            if type(i) != int:
                                raise ValueError
            else:
                raise ValueError

        if method == 'PUT':
            if {'fio', 'object_id'} in set(request.keys()):
                for key in request.keys():
                    if key not in {'fio', 'bio', 'contacts', 'office_id', 'object_id', 'subject_id', 'lesson_row_id'}:
                        raise ValueError
                    if key == 'fio' or key == 'bio' or 'contacts':
                        if type(request[key]) != str:
                            raise ValueError
                    if key == 'office_id' or key == 'object_id':
                        if type(request[key]) != int:
                            raise ValueError
                    if key == 'subject_id' or key == 'lesson_row_id':
                        for i in request[key]:
                            if type(i) != int:
                                raise ValueError
            else:
                raise ValueError
