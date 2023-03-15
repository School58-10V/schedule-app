import validators.abstract_validator


class LocationValidator(validators.abstract_validator.AbstractValidator):
    def __init__(self):
        required_keys = {'location_type', 'num_of_class'}
        allowed_keys = {'location_type', 'num_of_class', 'location_desc', 'profile', 'link', 'comment', 'equipment'}

        keys_types = {'location_type': str, 'num_of_class': int, 'location_desc': str,
                      'profile': str, 'link': str, 'comment': str, 'equipment': str}

        super(LocationValidator, self).__init__(required_keys, allowed_keys, keys_types)
