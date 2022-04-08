import json
from data_model.location import Location
from services.db_source_factory import DBFactory
from flask import Flask, request

app = Flask(__name__)
dbf = DBFactory()

# here will be your code

if __name__ == '__main__':
    app.run()