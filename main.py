import sqlite3
from contextlib import closing
from flask import Flask, render_template, g
app = Flask(__name__)


# DB configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = '1234'

app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# ----- Routes -----


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def regiter_user():
    return render_template('register.html')


"""
@app.route('/user/<username>')
def profile():
    return 0


def edit_profile():
    return 0


def my_signatures():
    return 0
"""

# ------------------


if __name__ == "__main__":
    app.run(debug=True)
    init_db()