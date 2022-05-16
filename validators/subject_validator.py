class SubjectValidator:

    def validate(self, request: dict, method: str):

        if method == 'POST':
            if request.keys() == ['subject_name']:
                if type(request['subject_name']) != str:
                    raise ValueError
            if request.keys() == ['subject_name', 'teachers']:
                if type(request['subject_name']) != str or type(request['teachers']) != list:
                    raise ValueError
                for teacher_id in request['teachers']:
                    if type(teacher_id) != int:
                        raise ValueError
            else:
                raise ValueError

        if method == 'PUT':
            if set(request.keys()) == {'object_id', 'subject_name'}:
                if type(request['object_id']) != int or type(request['subject_name']) != str:
                    raise ValueError
            if set(request.keys()) == {'object_id', 'subject_name', 'teachers'}:
                if type(request['object_id']) != int or type(request['subject_name']) != str or \
                        type(request['teachers']) == list:
                    raise ValueError
                for teacher_id in request['teachers']:
                    if type(teacher_id) != int:
                        raise ValueError
            else:
                raise ValueError
