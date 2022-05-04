from adapters.db_source import DBSource


class DBFactory:
    def __init__(self,
                 host="postgresql.aakapustin.ru",
                 password="VYRL!9XEB3yXQs4aPz_Q",
                 user="schedule_app", options="-c search_path=dbo,public"):
        self.__dbs = self.create_db_source(host, password, user, options=options)

    def get_db_source(self):
        return self.__dbs

    def create_db_source(self,
                         host,
                         password,
                         user,
                         options):
        return DBSource(host=host, password=password, user=user, options=options)

    def set_db_source(self,
                      host,
                      password,
                      user,
                      options):
        self.__dbs = DBSource(host=host, password=password, user=user, options=options)
