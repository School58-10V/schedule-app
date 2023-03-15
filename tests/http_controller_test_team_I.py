import json
from flask import Flask, request


app = Flask(__name__)

@app.route("/menu")
def hello_world():
    return "<p>Это будет основное меню</p>"

@app.route("/main")
def main():
    return "<p>короче спалили Лиду, она скайуокер</p>"


if __name__ == "__main__":
    app.run()