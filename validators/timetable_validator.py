class TimeTableValidator:

    def validate(self, request: dict, method: str):

        if method == 'POST':
            if request.keys() == ['time_table_year']:
                if type(request['time_table_year']) != int:
                    raise ValueError
            else:
                raise ValueError

        if method == 'PUT':
            if set(request.keys()) == {'time_table_year', 'object_id'}:
                if type(request['time_table_year']) != int or type(request['object_id']) != int:
                    raise ValueError
            else:
                raise ValueError
