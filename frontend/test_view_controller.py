from flask import request, render_template
from schedule_app import app

BASE_PATH = '127.0.0.1:5000/api/v1'


@app.route('/test', methods=['GET'])
def test_page():
    return render_template('test.html')
