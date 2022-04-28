from flask import Flask, request

from services.db_source_factory import DBFactory

app = Flask(__name__)
dbf = DBFactory()

@app.before_request
def login():
    req = request.host
