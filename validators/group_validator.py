class GroupValidate:

    def __init__(self, request: dict, method: str):
        self.request = request
        self.method = method

    def validate(self):
        try:

            if self.method == 'POST':
                if set(self.request.keys()) == {'teacher_id', 'class_letter', 'grade', 'profile_name'}:
                    for key in self.request.keys():
                        if key == 'teacher_id' or key == 'grade':
                            if type(self.request[key]) != int:
                                raise ValueError
                        if key == 'class_letter' or key == 'profile_name':
                            if type(self.request[key]) != str:
                                raise ValueError
                else:
                    raise ValueError

            if self.method == 'PUT':
                if set(self.request.keys()) == {'teacher_id', 'class_letter', 'grade', 'profile_name', 'object_id'}:
                    if type(self.request['teacher_id']) != int:
                        raise ValueError
                    if type(self.request['class_letter']) != str:
                        raise ValueError
                    if type(self.request['grade']) != int:
                        raise ValueError
                    if type('profile_name') != str:
                        raise ValueError
                    if type(self.request['object_id']) != int:
                        raise ValueError
                else:
                    raise ValueError

        except ValueError:
            return '', 400