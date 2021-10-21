from random import randrange


class Matter:
    def __init__(self, name):
        self.__name = name
        self.__id = randrange(1, 350000)

    @property
    def get_id(self):
        return self.__id

    @property
    def get_name(self):
        return self.__name
