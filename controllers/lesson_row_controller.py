import json
from data_model.lesson_row import LessonRow
from services.db_source_factory import DBFactory
from flask import Flask, request

app = Flask(__name__)
dbf = DBFactory()

# here will be your code

if __name__ == '__main__':
    app.run()