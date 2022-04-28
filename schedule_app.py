from flask import Flask
from services.db_source_factory import DBFactory

dbf = DBFactory()
app = Flask("Schedule-app")
app.config["db_factory"] = dbf

