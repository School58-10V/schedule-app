from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class StudentName(FlaskForm):
    name = StringField('Полное имя пользователя:', validators=[DataRequired()])
    date = StringField('День недели:', validators=[DataRequired()])
    submit = SubmitField('Найти расписание')
