import datetime
from flask import Flask, render_template, redirect
from data.jobs import Jobs
from data.users import User
from data import db_session
from data.login_form import LoginForm
from data.job_form import JobForm
from data.register_form import RegisterForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

profs = ['инженер', 'пилот', 'врач', 'гляциолог', 'метеорит', 'штурман']


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    db_sess = db_session.create_session()
    return render_template('works_log.html', jobs=db_sess.query(Jobs).all())


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        existing_user = db_sess.query(User).filter(User.email == form.email.data).first()
        if existing_user:
            return render_template('register.html',
                                   title='Регистрация',
                                   message="Введенный e-mail уже зарегистрирован",
                                   form=form)
        new_user = User()
        new_user.name = form.name.data
        new_user.surname = form.surname.data
        new_user.age = form.age.data
        new_user.position = form.position.data
        new_user.speciality = form.speciality.data
        new_user.address = form.address.data
        new_user.email = form.email.data
        new_user.modified_date = datetime.datetime.now()
        new_user.set_password(form.password.data)

        db_sess.add(new_user)
        db_sess.commit()
        login_user(new_user, remember=form.remember_me.data)
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/addjob', methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        new_job = Jobs()
        new_job.job = form.job.data
        new_job.team_leader = form.team_leader.data
        new_job.work_size = form.work_size.data
        new_job.collaborators = form.collaborators.data
        new_job.is_finished = form.is_finished.data
        new_job.start_date = datetime.datetime.now()
        current_user.jobs.append(new_job)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('add_job.html', title='Adding a job', form=form)


if __name__ == '__main__':
    db_session.global_init('db/db.db')
    port = int(os.environ.get("PORT", 5000))
    app.run(port=port, host='0.0.0.0', debug=False)
