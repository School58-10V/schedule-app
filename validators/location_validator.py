class LocationValidator:

    def validate(self, request: dict, method: str):

        required_keys = {'location_type', 'num_of_class'}
        allowed_keys = {'location_type', 'num_of_class', 'location_desc', 'profile', 'link', 'comment', 'equipment'}

        if method == 'PUT':
            required_keys.add('object_id')
            allowed_keys.add('object_id')

        for key in required_keys:
            if key not in request.keys():
                raise ValueError

        for key in request.keys():
            if key not in allowed_keys:
                raise ValueError
            if key == 'location_type' or key == 'location_desc' or key == 'profile' or key == 'link' \
                    or key == 'comment' or key == 'equipment':
                if type(request[key]) != str:
                    raise ValueError
            if key == 'num_of_class':
                if type(request[key]) != int:
                    raise ValueError
