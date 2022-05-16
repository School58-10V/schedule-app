class StudentValidator:

    def validate(self, request: dict, method: str):

        if method == 'POST':
            if {'full_name', 'date_of_birth'} in set(request.keys()):
                for key in request.keys():
                    if key not in {'full_name', 'date_of_birth', 'contacts', 'bio'}:
                        raise ValueError
                    if key == 'full_name' or key == 'contacts' or key == 'bio':
                        if type(request[key]) != str:
                            raise ValueError
                    if key == 'date_of_birth':
                        if type(request[key]) != int:
                            raise ValueError
            else:
                raise ValueError

        if method == 'POST':
            if {'full_name', 'date_of_birth', 'object_id'} in set(request.keys()):
                for key in request.keys():
                    if key not in {'full_name', 'date_of_birth', 'contacts', 'bio', 'object_id'}:
                        raise ValueError
                    if key == 'full_name' or key == 'contacts' or key == 'bio':
                        if type(request[key]) != str:
                            raise ValueError
                    if key == 'date_of_birth' or key == 'object_id':
                        if type(request[key]) != int:
                            raise ValueError
            else:
                raise ValueError
