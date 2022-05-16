class GroupValidator:

    def validate(self, request: dict, method: str):

        if method == 'POST':
            if set(request.keys()) == {'teacher_id', 'class_letter', 'grade', 'profile_name'}:
                for key in request.keys():
                    if key == 'teacher_id' or key == 'grade':
                        if type(request[key]) != int:
                            raise ValueError
                    if key == 'class_letter' or key == 'profile_name':
                        if type(request[key]) != str:
                            raise ValueError
            else:
                raise ValueError

        if method == 'PUT':
            if set(request.keys()) == {'teacher_id', 'class_letter', 'grade', 'profile_name', 'object_id'}:
                for key in request.keys():
                    if key == 'teacher_id' or key == 'grade' or key == 'object_id':
                        if type(request[key]) != int:
                            raise ValueError
                    if key == 'class_letter' or key == 'profile_name':
                        if type(request[key]) != str:
                            raise ValueError
            else:
                raise ValueError
