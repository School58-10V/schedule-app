from adapters.db_adapter import DbAdapter


adapter = DbAdapter()
adapter.update("TimeTables", {"object_id": 1, "time_table_year": 5654})
