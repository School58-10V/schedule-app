class TimeTableValidate:

    def __init__(self, request: dict, method: str):
        self.request = request
        self.method = method

    def validate(self):

            if self.method == 'POST':
                if self.request.keys() == ['time_table_year']:
                    if type(self.request['time_table_year']) != int:
                        raise ValueError
                else:
                    raise ValueError

            if self.method == 'PUT':
                if set(self.request.keys()) == {'time_table_year', 'object_id'}:
                    if type(self.request['time_table_year']) != int or type(self.request['object_id']) != int:
                        raise ValueError
                else:
                    raise ValueError