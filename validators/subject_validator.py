class SubjectValidate:

    def __init__(self, request: dict, method: str):
        self.request = request
        self.method = method

    def validate(self):

            if self.method == 'POST':
                if self.request.keys() == ['subject_name']:
                    if type(self.request['subject_name']) != str:
                        raise ValueError
                if self.request.keys() == ['subject_name', 'teachers']:
                    if type(self.request['subject_name']) != str or type(self.request['teachers']) != list:
                        raise ValueError
                    for teacher_id in self.request['teachers']:
                        if type(teacher_id) != int:
                            raise ValueError
                else:
                    raise ValueError

            if self.method == 'PUT':
                if set(self.request.keys()) == {'object_id', 'subject_name'}:
                    if type(self.request['object_id']) != int or type(self.request['subject_name']) != str:
                        raise ValueError
                if set(self.request.keys()) == {'object_id', 'subject_name', 'teachers'}:
                    if type(self.request['object_id']) != int or type(self.request['subject_name']) != str or \
                            type(self.request['teachers']) == list:
                        raise ValueError
                    for teacher_id in self.request['teachers']:
                        if type(teacher_id) != int:
                            raise ValueError
                else:
                    raise ValueError