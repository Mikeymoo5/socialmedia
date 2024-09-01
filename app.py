from flask import Flask, render_template
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, PasswordField
from flask_bootstrap import Bootstrap5

import sqlite3

db = sqlite3.connect("database.db")
cursor = db.cursor()

app = Flask(__name__)
app.secret_key = "apple"
bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)
# Make the user login table if it does not exist
cursor.execute('''CREATE TABLE IF NOT EXISTS users (username text, password text)''')

@app.route("/")
def home_page():
    return render_template("index.html", page_title="Home")
    # return "<p>Welcome!</p>"

@app.route("/signup", methods=['GET', 'POST'])
def signup_page():
    form = GenericUserForm()
    if form.validate_on_submit():
        usr = form.usr.data
        password = form.password.data
        cursor = sqlite3.connect("database.db").cursor()
        try:
            cursor.execute(f'''SELECT username FROM users WHERE username={usr} AND password={password} ''')
        except: 
            return "<p>Account already exists</p>"
        cursor.execute(f'''INSERT INTO users VALUES ({usr}, {password}))''')
    return render_template("form.html", page_title="Signup", form=form)

@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = GenericUserForm()
    if form.validate_on_submit():
        usr = form.usr.data
        password = form.password.data
        cursor = sqlite3.connect("database.db").cursor()
        try:
            cursor.execute(f'''SELECT username FROM users WHERE username={usr} AND password={password} ''')
        except: 
            return "<p>Account name or password is incorrect</p>"
        return "<p>LOGGED IN</p>"
    return render_template("form.html", page_title="Login", form=form)

class GenericUserForm(FlaskForm):
    usr = StringField("Username")
    password = PasswordField("Password")
    submit = SubmitField("Submit")