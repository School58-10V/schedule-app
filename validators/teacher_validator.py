class TeacherValidator:

    def validate(self, request: dict, method: str):

        required_keys = {'fio'}
        allowed_keys = {'fio', 'bio', 'contacts', 'office_id', 'subject_id', 'lesson_row_id'}

        if method == 'PUT':
            required_keys.add('object_id')
            allowed_keys.add('object_id')

        for key in required_keys:
            if key not in request.keys():
                print(key, request.keys(), key in request.keys())
                print('TYT')
                raise ValueError

        for key in request.keys():
            if key not in allowed_keys:
                print('tyt')
                raise ValueError
            if key == 'fio' or key == 'bio' or key == 'contacts':
                if type(request[key]) != str:
                    print('fio')
                    raise ValueError
            if key == 'office_id':
                if type(request[key]) != int:
                    print('int')
                    raise ValueError
            if key == 'subject_id' or key == 'lesson_row_id':
                for i in request[key]:
                    if type(i) != int:
                        print('subject')
                        raise ValueError
