class TeacherValidate:

    def __init__(self, request: dict, method: str):
        self.request = request
        self.method = method

    def validate(self):
        try:
            given_keys = set()
            for i in self.request.keys():
                given_keys.add(i)

            if 'lesson_row_id' in given_keys:
                given_keys.remove('lesson_row_id')

            if 'subject_id' in given_keys:
                given_keys.remove('subject_id')

            if self.method == 'PUT':
                if 'object_id' in given_keys:
                    if type(self.request['object_id']) != int:
                        raise ValueError
                else:
                    raise ValueError
                given_keys.remove('object_id')

            if given_keys == {'bio', 'contacts', 'fio', 'office_id'}:
                for i in self.request.keys():
                    if i == 'bio' or i == 'fio':
                        if type(self.request[i]) != str:
                            raise ValueError
                    if i == 'contacts':
                        if type(self.request[i]) != str and type(self.request[i]) != bool:
                            raise ValueError
                    if i == 'office_id':
                        if type(self.request[i]) != int:
                            raise ValueError
                    if i == 'lesson_row_id':
                        if type(self.request[i]) == list:
                            for g in self.request[i]:
                                if type(g) != int:
                                    raise ValueError
                        else:
                            raise ValueError
                    if i == 'subject_id':
                        if type(self.request[i]) == list:
                            for g in self.request[i]:
                                if type(g) != int:
                                    raise ValueError
                        else:
                            raise ValueError
            else:
                raise ValueError

        except ValueError:
            return '', 400