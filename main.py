from flask import Flask, render_template
from data.jobs import Jobs
from data import db_session


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

profs = ['инженер', 'пилот', 'врач', 'гляциолог', 'метеорит', 'штурман']


@app.route('/')
def index():
    db_sess = db_session.create_session()
    return render_template('works_log.html', jobs=db_sess.query(Jobs).all())


if __name__ == '__main__':
    db_session.global_init('db/db.db')
    app.run(port=8080, host='127.0.0.1', debug=True)
