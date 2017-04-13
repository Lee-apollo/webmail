from webapp import app
from flask import Flask, abort, redirect, render_template, session, url_for, request, escape
from werkzeug.utils import secure_filename
#from app import db_interface.add_user as add_user

from webapp import db_interface
from db_interface import add_user, is_login_valid, list_users, get_emails, list_emails, get_user_id, get_user

def hash(passwd):
    return passwd


@app.route('/')
@app.route('/index')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = escape(session['user_id'])
    emails = [email.as_dict() for email in get_emails(user_id)]
    print("USER ID: %s" % user_id)
    user = get_user(user_id)

    return render_template("index.html", title="Home", user=user, mails=emails, logged_in = True)


def log_the_user_in(username):
    #Modify session - log in user and redirect to index
    if request.method == 'POST':
        session['user_id'] = get_user_id( login = request.form['username'] )
    return redirect(url_for('index'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    # If user is already logged in, redirect to index
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    error = None
    if request.method == 'POST':
        if is_login_valid(request.form['username'],
            hash(request.form['password'])):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'

    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', message=error)


@app.route('/logout', methods=['GET'])
def logout():
    error = None
    if 'user_id' in session:
            #session.pop('username', None)
        del(session['user_id'])
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
            return render_template("registration.html", message="Invalid values")

        add_user(login = request.form["username"],
                 name = request.form["name"],
                 pass_hash = hash(request.form["password"]))

        # Show register OK
        return render_template("registration.html", message="Registration OK")
        #return redirect(url_for('success'))
    else:
        return "Unknown method"

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
