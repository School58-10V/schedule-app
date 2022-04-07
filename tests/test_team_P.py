from flask import Flask, request

app = Flask(__name__)


@app.route("/main")
def main_page():
    return "<p>Это главная страница</p>"


@app.route("/main")
def index():
    return '<h1>Hello world</h1>'


@app.route("/user/<name>")
def user(name):
    return '<h1>Hi, %s!</h1>' % name


if __name__ == '__main__':
    app.run(debug=True)
