from flask import Flask
from services.db_source_factory import DBFactory
from config import Configuration


cfg = Configuration()
dbf = DBFactory()
dbf.set_db_source(host=cfg.get_configuration()["host"], password=cfg.get_configuration()["password"],
                  user=cfg.get_configuration()["user"])

app = Flask("Schedule-app")
app.config["db_factory"] = dbf

