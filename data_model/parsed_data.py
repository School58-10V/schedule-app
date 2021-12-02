class ParsedData:
    def __init__(self, error, model):
        self.__error = error
        self.__model = model

    def get_error(self):
        return self.__error

    def get_model(self):
        return self.__model

    def has_error(self):
        return self.__error is not None
