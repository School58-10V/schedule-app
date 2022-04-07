from flask import Flask, request

app = Flask(__name__)


@app.route("/main")
def main_page():
    return "<p>Это главная страница</p>"


@app.route("/post", methods=["POST", "GET"])
def hello_post():
    data = request.get_data().decode('utf8')
    return {"вы прислали": data}


if __name__ == '__main__':
    app.run()
