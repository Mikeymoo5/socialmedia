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

@app.route("/signup")
def signup_page():
    form = GenericUserForm()
    return render_template("form.html", page_title="Signup", form=form)

@app.route("/login")
def login_page():
    form = GenericUserForm()
    return render_template("form.html", page_title="Login", form=form)

class GenericUserForm(FlaskForm):
    usr = StringField("Username")
    password = PasswordField("Password")
    submit = SubmitField("Submit")