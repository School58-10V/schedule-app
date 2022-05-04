class StudentValidate:

    def __init__(self, request: dict, method: str):
        self.request = request
        self.method = method

    def validate(self):
        try:
            if self.method == 'POST':
                if {'full_name', 'date_of_birth'} in set(self.request.keys()):
                    for key in self.request.keys():
                        if key not in {'full_name', 'date_of_birth', 'contacts', 'bio'}:
                            raise ValueError
                        if key == 'full_name' or key == 'contacts' or key == 'bio':
                            if type(self.request[key]) != str:
                                raise ValueError
                        if key == 'date_of_birth':
                            if type(self.request[key]) != int:
                                raise ValueError
            if self.method == 'POST':
                if {'full_name', 'date_of_birth', 'object_id'} in set(self.request.keys()):
                    for key in self.request.keys():
                        if key not in {'full_name', 'date_of_birth', 'contacts', 'bio', 'object_id'}:
                            raise ValueError
                        if key == 'full_name' or key == 'contacts' or key == 'bio':
                            if type(self.request[key]) != str:
                                raise ValueError
                        if key == 'date_of_birth' or key == 'object_id':
                            if type(self.request[key]) != int:
                                raise ValueError
        except ValueError:
            return '', 400