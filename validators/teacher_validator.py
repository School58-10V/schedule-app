from werkzeug.exceptions import BadRequest


class TeacherValidate:

    def __init__(self, request: dict, method: str):
        self.request = request
        self.method = method

    def validate(self, request, method):
        f = True
        given_keys = set()
        keys = {'bio', 'contacts', 'fio', 'office_id'}

        for i in request.keys():
            given_keys.add(i)

        if 'lesson_row_id' in given_keys:
            given_keys.remove('lesson_row_id')

        if 'subject_id' in given_keys:
            given_keys.remove('subject_id')

        if method == 'PUT':
            if 'object_id' in given_keys:
                if type(request['object_id']) != int:
                    f = False
            else:
                f = False

        if given_keys != keys:
            f = False

        for i in request.keys():
            if i == 'bio' or i == 'fio':
                if type(request[i]) != str:
                    f = False
            if i == 'contacts':
                if type(request[i]) != str and type(request[i]) != bool:
                    f = False
            if i == 'lesson_row_id' or i == 'subject_id':
                if type(request[i]) == list:
                    for g in request[i]:
                        if type(g) != int:
                            f = False
            else:
                f = False

        try:
            if f:
                return True
        except BadRequest:
            return '', 400
