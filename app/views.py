from app import app

from flask import Flask, redirect, render_template, session, url_for, request
from werkzeug.utils import secure_filename

@app.route('/')
@app.route('/index')
def index():
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

    user = {'name': 'Petr'}  # fake user
    return render_template("index.html", title="Home", user=user, mails=mails)

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
	return render_template("login.html", message=None)
    elif request.method == "POST":
        if request.form["username"] and request.form["passwd"]:
         
@app.route('/registration', methods=["GET", "POST"])
def registration():
    if request.method == "GET":
        #Show registration form
        return render_template("registration.html")
    elif request.method == "POST":
        # check input data

        if request.form["name"] == "" or request.form["passwd"] == "":
            # Show error message and stay on registration page
            return "ERROR"
        else:
            # Show register OK
            return render_template("registration.html")
    else:
        return "Unknown method"


########

         
def valid_login(username, password):
    return False;

def log_the_user_in(username):
    return ("User %s loged in" % (username))

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/uploaded_file.txt/' + secure_filename(f.filename))



from flask import abort, redirect, url_for


## Redirect 
@app.route('/')
def index():
    return redirect(url_for('login'))


## Errors
@app.route('/error') # /login
def login():
    abort(401)
    this_is_never_executed()
