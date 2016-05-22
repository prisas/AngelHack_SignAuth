# from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from flask import Flask, render_template, redirect, url_for, flash, request
from datetime import datetime
from random import randint


app = Flask(__name__)

db = create_engine('sqlite:///signature.db')
db.echo = False
metadata = MetaData(db)

status_connected = False
rs = []


users = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('email', String, unique=True),
    Column('password', String),
    Column('img_id', Integer)
)
#users.create()

log = Table('logs', metadata,
    Column('id', Integer, ForeignKey("users.id"), primary_key=True),
    Column('date_time', Text, primary_key=True),
    Column('whereFrom', String),
    Column('accepted', Boolean),
    Column('img_id', Integer)
)
#log.create()


def run(stmt):
    rs = stmt.execute()
    for row in rs:
        return row


def renderLogData(stmt):
    rs = stmt.execute()
    for row in rs:
        flash(row)
    return


# ----- Routes -----

@app.route('/')
def index():
    return render_template('index.html', status=status_connected)


@app.route('/login/')
def login_user():
    return render_template('login.html')


@app.route('/register')
def register_user():
    return render_template('register.html')


@app.route('/my_log')
def show_log():
    global status_connected
    if status_connected:
        global rs
        s = log.select(log.c.id == rs[0])
        renderLogData(s)
        return render_template('log_entry.html')
    else:
        return render_template('403.html')


@app.route('/home', methods=['GET', 'POST'])
def treat_login():
    if request.method == 'POST':
        my_email = request.form['email']
        s = users.select(users.c.email == my_email)
        global rs
        rs = run(s)
        print(rs)
        if rs is None:
            flash('Invalid email or password', 'error')
            return redirect(url_for('login_user'))
        else:
            my_password = request.form['password']
            if my_password == rs[3]:
                global status_connected
                status_connected = True
                return redirect(url_for('show_log'))
            else:
                flash('Invalid email or password', 'error')
                return redirect(url_for('login_user'))


@app.route('/registering', methods=['GET', 'POST'])
def treat_register():
    if request.method == 'POST':
        my_email = request.form['email']
        s = users.select(users.c.email == my_email)
        rs = run(s)
        if rs is None:
            my_password = request.form['password']
            my_password2 = request.form['password2']
            if my_password == my_password2:
                v0 = randint(0, 3)
                v1 = randint(0, 3)
                v2 = randint(0, 3)
                v3 = randint(0, 3)
                new_signature = v0 * 1000 + v1 * 100 + v2 * 10 + v3
                i = users.insert()
                i.execute(name=request.form['name'], email=my_email, password=my_password, img_id=new_signature)
                flash('Successfully registered, now you can Log In!', 'success'),
                return render_template('login.html')
            else:
                flash('Your passwords do not match!', 'error')
                return redirect(url_for('register_user'))
        else:
            flash('This email is already registered!', 'error')
            return redirect(url_for('login_user'))


@app.route('/gensignature')
def add_log_entry():
    z = 0
    global rs
    s = users.select(users.c.id == rs[0])
    rs = run(s)
    i = log.insert()
    while z < 10:
        v0 = randint(0, 3)
        v1 = randint(0, 3)
        v2 = randint(0, 3)
        v3 = randint(0, 3)
        z += 1
        new_signature = v0 * 1000 + v1 * 100 + v2 * 10 + v3
        if new_signature == rs[4]:
            i.execute(id=rs[0], date_time=str(datetime.now()), whereFrom='Barcelona', accepted=True, img_id=new_signature)
            return redirect(url_for('show_log'))
    i.execute(id=rs[0], date_time=str(datetime.now()), whereFrom='Barcelona', accepted=False, img_id=new_signature)
    return redirect(url_for('show_log'))


@app.route('/showsimulation', methods=['GET', 'POST'])
def showSignature():
    global rs
    # My signature
    ourselection = int(rs[4])
    myv0 = ourselection / 1000
    myv1 = (ourselection % 1000) / 100
    myv2 = (ourselection % 100) / 10
    myv3 = ourselection % 10
    # DB signature
    selected_image = int(request.form['dataCross'])
    logv0 = selected_image / 1000
    logv1 = (selected_image % 1000) / 100
    logv2 = (selected_image % 100) / 10
    logv3 = selected_image % 10
    return render_template('splines.html', myv0=myv0, myv1=myv1, myv2=myv2, myv3=myv3, logv0=logv0, logv1=logv1, logv2=logv2, logv3=logv3)


@app.route('/backanimation')
def wheretoback():
    if status_connected:
        return redirect(url_for('show_log'))
    else:
        return redirect(url_for('login_user'))


@app.route('/logout')
def logout():
    global status_connected
    status_connected = False
    return redirect(url_for('index'))


@app.errorhandler(403)
def page_forbidden(e):
    return render_template('403.html'), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(IndexError)
def internal_error(e):
    return render_template('403.html')


if __name__ == "__main__":
    app.secret_key = '1234'
    app.run(debug=True)
