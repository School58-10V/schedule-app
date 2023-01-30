from flask import Flask
from services.db_source_factory import DBFactory
from services.validator_factory import ValFactory
from config import Configuration
from flask_cors import CORS

cfg = Configuration()
schedule_dbf = DBFactory(host=cfg.get_configuration()["schedule_database"]["host"],
                        password=cfg.get_configuration()["schedule_database"]["password"],
                        user=cfg.get_configuration()["schedule_database"]["user"],
                        options=cfg.get_configuration()["schedule_database"]["options"])
auth_dbf = DBFactory(host=cfg.get_configuration()["user_database"]["host"],
                    password=cfg.get_configuration()["user_database"]["password"],
                    user=cfg.get_configuration()["user_database"]["user"],
                    options=cfg.get_configuration()["user_database"]["options"])

val_factory = ValFactory()

app = Flask("Schedule-app")
CORS(app)
app.config["schedule_db_source"] = schedule_dbf.get_db_source()
app.config["auth_db_source"] = auth_dbf.get_db_source()
app.config['validators_factory'] = val_factory
