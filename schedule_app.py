from flask import Flask
from services.db_source_factory import DBFactory
from config import Configuration


cfg = Configuration.configuration()
dbf = DBFactory()
dbf.set_db_source(host=cfg["host"], password=cfg["password"], user=cfg["user"])

app = Flask("Schedule-app")
app.config["db_factory"] = dbf

