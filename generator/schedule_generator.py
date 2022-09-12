from schedule_app import app

from data_model.student import Student

# class TestGenerator:
#     def __init__(self):

if __name__ == '__main__':
    elements = Student.get_all(app.config.get('schedule_db_source'))
    print(elements)