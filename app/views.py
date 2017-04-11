from app import app

from flask import Flask, abort, redirect, render_template, session, url_for, request, escape
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy

# Flask-SQLAlchemy
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ztelesneny-neuspech.db"
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)

class User(db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    passwd = db.Column(db.Text)
    name = db.Column(db.Text)

    def __init__(self, username, passwd, name):
        self.username = username
        self.name = name
        self.passwd = passwd

class Message(db.Model):

    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    unread = db.Column(db.Integer)
    addrTo = db.Column(db.Text)
    addrFrom = db.Column(db.Text)
    subject = db.Column(db.Text)
    body = db.Column(db.Text)

    def __init__(self, user_id, addrTo, addFrom, subject, body):
        self.user_id = user_id
        self.unread = 1 #TODO Add better boolean expresion
        self.addrTo = addrTo
        self.addrFrom = addrFrom
        self.subject = subject
        self.body = body





def getEmails(username):
    mails = [ # fake array of emails
        { "from" : "Petr@fake-email.com",
          "to": "Petr@ztelesneny-neuspech.com",
          "subject" : "Re: Hello world!",
          "body" : "Hi mate. How are you?"
        },
        { "from" : "spam@spam.com",
          "to": "Petr@ztelesneny-neuspech.com",
          "subject" : "Buy this shit!",
          "body" : "XYZ"
        },
        { "from" : "mail@ztelezneny-neuspech.cz",
          "to": "Petr@ztelesneny-neuspech.com",
          "subject" : "Welcome to the best site ever!",
          "body" : "Hi Petr"
        }
    ]
    return mails


@app.route('/')
@app.route('/index')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))

    
    username = escape(session['username'])
    #user = {'name': 'Petr'}  # fake user

    user = {'name' : username}
    emails = getEmails(username)

    return render_template("index.html", title="Home", user=user, mails=emails, logged_in = True)


#users = {{'name' : 'Petr', 'password' = 'pass123'}, {'name' : 'Test', 'password' = 'heslo'}}
    
users = { "Petr" : "pass123", "test": "heslo"}
    
def valid_login(username, password):
    
    if username in users and users[username] == password:
        return True
    return False


def log_the_user_in(username):
    #Modify session - log in user and redirect to index

    if request.method == 'POST':
        session['username'] = request.form['username']
    
    return redirect(url_for('index'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    
    # If user is already logged in, redirect to index
    if 'username' in session:
        return redirect(url_for('index'))
    
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'

    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', message=error)


@app.route('/logout', methods=['GET'])
def logout():
    error = None
    if 'username' in session:
            #session.pop('username', None)
        del(session['username'])
    return redirect(url_for('index'))


@app.route('/registration', methods=["GET", "POST"])
def registration():
    if request.method == "GET":
        #Show registration form
        return render_template("registration.html")
    elif request.method == "POST":
        # check input data

        if request.form["username"] == "" or request.form["password"] == "" or request.form["name"] == "":
            # Show error message and stay on registration page
            return render_template("registration.html", error="Invalid values")

        registrant = User(request.form["username"], request.form["password"], request.form["name"])
        db.session.add(registrant)
        db.session.commit()

        # Show register OK
        return redirect(url_for('success'))
    else:
        return "Unknown method"

@app.route('/success', methods=["GET"])
def success():
    users = User.query.all()
    return render_template('login.html', message=users)

########

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/uploaded_file.txt/' + secure_filename(f.filename))

## Errors
@app.route('/error') # /login
def error():
    abort(401)
    this_is_never_executed()
