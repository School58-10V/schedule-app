class StudentValidator:

    def validate(self, request: dict, method: str):

        required_keys = {'full_name', 'date_of_birth'}
        allowed_keys = {'full_name', 'date_of_birth', 'contacts', 'bio'}

        if method == 'PUT':
            required_keys.add('object_id')
            allowed_keys.add('object_id')

        for key in required_keys:
            if key not in request.keys():
                raise ValueError

        for key in request.keys():
            if key not in allowed_keys:
                raise ValueError
            if key == 'full_name' or key == 'contacts' or key == 'bio':
                if type(request[key]) != str:
                    raise ValueError
            if key == 'date_of_birth':
                if type(request[key]) != int:
                    raise ValueError
