from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, StringField, IntegerField, DateTimeField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    job = StringField('Название работы', validators=[DataRequired()])
    team_leader = IntegerField('ID лидера команды', validators=[DataRequired()])
    work_size = IntegerField('Долгость работы (ч)', validators=[DataRequired()])
    collaborators = StringField('Коллабораторы', validators=[DataRequired()])
    # start_date = DateTimeField('Дата начала', validators=[DataRequired()])
    # end_date = DateTimeField('Дата конца', validators=[DataRequired()])
    is_finished = BooleanField('Закончена ли')
    submit = SubmitField('Добавить')
