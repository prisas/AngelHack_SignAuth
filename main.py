# from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from flask import Flask, render_template, redirect, url_for, flash, request

app = Flask(__name__)

db = create_engine('sqlite:///signature.db')
db.echo = False
metadata = MetaData(db)


users = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('email', String, unique=True),
    Column('password', String),
    Column('img_id', Integer)
)
#users.create()


def run(stmt):
    rs = stmt.execute()
    for row in rs:
        return row


# ----- Routes -----

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login_user():
    return render_template('login.html')


@app.route('/register')
def register_user():
    return render_template('register.html')


@app.route('/home', methods=['GET', 'POST'])
def treat_login():
    if request.method == 'POST':
        my_email = request.form['email']
        s = users.select(users.c.email == my_email)
        alreadyThere = run(s)
        print(alreadyThere)
        if alreadyThere is None:
            flash('Invalid email or password', 'error')
            return redirect(url_for('login_user'))
        else:
            my_password = request.form['password']
            s = users.select(users.c.email == my_email)
            passwordCorrect = run(s)
            if my_password == passwordCorrect[3]:
                return render_template('home.html')
            else:
                flash('Invalid email or password', 'error')
                return redirect(url_for('login_user'))


@app.route('/registering', methods=['GET', 'POST'])
def treat_register():
    if request.method == 'POST':
        my_email = request.form['email']
        s = users.select(users.c.email == my_email)
        alreadyThere = run(s)
        if alreadyThere is None:
            my_password = request.form['password']
            my_password2 = request.form['password2']
            if my_password == my_password2:
                i = users.insert()
                i.execute(name=request.form['name'], email=my_email, password=my_password)
                flash('Successfully registered, now you can Log In!', 'success'),
                return render_template('login.html')
            else:
                flash('Your passwords do not match!', 'error')
                return redirect(url_for('register_user'))
        else:
            flash('This email is already registered!', 'error')
            return redirect(url_for('login_user'))


if __name__ == "__main__":
    app.secret_key = '1234'
    app.run(debug=True)
