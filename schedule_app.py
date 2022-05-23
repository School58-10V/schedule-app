from flask import Flask
from services.db_source_factory import DBFactory
from config import Configuration

cfg = Configuration()
schedule_dbf = DBFactory()
schedule_dbf.set_db_source(host=cfg.get_configuration()["schedule_database"]["host"],
                           password=cfg.get_configuration()["schedule_database"]["password"],
                           user=cfg.get_configuration()["schedule_database"]["user"],
                           options=cfg.get_configuration()["schedule_database"]["options"])
auth_dbf = DBFactory()
auth_dbf.set_db_source(host=cfg.get_configuration()["user_database"]["host"],
                       password=cfg.get_configuration()["user_database"]["password"],
                       user=cfg.get_configuration()["user_database"]["user"],
                       options=cfg.get_configuration()["user_database"]["options"])

app = Flask("Schedule-app")
app.config["schedule_db_source"] = schedule_dbf.get_db_source()
app.config["auth_db_source"] = auth_dbf.get_db_source()