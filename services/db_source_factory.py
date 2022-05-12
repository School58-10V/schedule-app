from adapters.db_source import DBSource


class DBFactory:
    def __init__(self,
                 host="postgresql.aakapustin.ru",
                 password="VYRL!9XEB3yXQs4aPz_Q",
                 user="schedule_app"):
        self.__dbs = self.create_db_source(host, password, user)

    def get_db_source(self):
        return self.__dbs

    def create_db_source(self,
                         host,
                         password,
                         user):
        return DBSource(host=host, password=password, user=user)

    def set_db_source(self,
                      host,
                      password,
                      user):
        self.__dbs = DBSource(host=host, password=password, user=user)
