from werkzeug.exceptions import BadRequest


class TeacherValidate:

    def __init__(self, request: dict, method: str):
        self.request = request
        self.method = method

    def validate(self):
        f = True
        given_keys = set()
        keys = {'bio', 'contacts', 'fio', 'office_id'}

        for i in self.request.keys():
            given_keys.add(i)

        if 'lesson_row_id' in given_keys:
            given_keys.remove('lesson_row_id')

        if 'subject_id' in given_keys:
            given_keys.remove('subject_id')

        if self.method == 'PUT':
            if 'object_id' in given_keys:
                if type(self.request['object_id']) != int:
                    f = False
            else:
                f = False

        if given_keys != keys:
            f = False

        for i in self.request.keys():
            if i == 'bio' or i == 'fio':
                if type(self.request[i]) != str:
                    f = False
            if i == 'contacts':
                if type(self.request[i]) != str and type(self.request[i]) != bool:
                    f = False
            if i == 'lesson_row_id' or i == 'subject_id':
                if type(self.request[i]) == list:
                    for g in self.request[i]:
                        if type(g) != int:
                            f = False
            else:
                f = False

        try:
            if f:
                return True
        except BadRequest:
            return '', 400
