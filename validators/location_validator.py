class LocationValidator:

    def validate(self, request: dict, method: str):

        if method == 'POST':
            if {'location_type', 'num_of_class'} in set(request.keys()):
                for key in request.keys():
                    if key not in {'location_type', 'num_of_class', 'location_desc', 'profile', 'link',
                                   'comment', 'equipment'}:
                        raise ValueError
                    if key == 'location_type' or key == 'location_desc' or key == 'profile' or key == 'link' \
                            or key == 'comment' or key == 'equipment':
                        if type(request[key]) != str:
                            raise ValueError
                    if key == 'num_of_class':
                        if type(request[key]) != int:
                            raise ValueError
            else:
                raise ValueError

        if method == 'PUT':
            if {'location_type', 'num_of_class', 'object_id'} in set(request.keys()):
                for key in request.keys():
                    if key not in {'location_type', 'num_of_class', 'location_desc', 'profile', 'link',
                                   'comment', 'equipment', 'object_id'}:
                        raise ValueError
                    if key == 'location_type' or key == 'location_desc' or key == 'profile' or key == 'link' \
                            or key == 'comment' or key == 'equipment':
                        if type(request[key]) != str:
                            raise ValueError
                    if key == 'num_of_class' or key == 'object_id':
                        if type(request[key]) != int:
                            raise ValueError
            else:
                raise ValueError

