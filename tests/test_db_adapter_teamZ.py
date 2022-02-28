from adapters.db_source import DBSource


source = DBSource(dbname='schedule_app', user='schedule_app',
                  password='VYRL!9XEB3yXQs4aPz_Q', host='postgresql.aakapustin.ru')
source.connect()
source.update("TimeTables", {"object_id": 11, "time_table_year": 2099})
source.delete("TimeTables", 11)
