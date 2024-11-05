from flask import Flask, request, render_template, redirect, url_for, abort, session
from flask import flash
from flask_sqlalchemy import SQLAlchemy
from Forms import RegisterForm, LoginForm, PreferenceForm

# make sure the script's directory is in Python's import path
# this is only required when run from a different directory
import os
import sys
script_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(script_dir)
# once script directory is in path, import Contact and ContactForm
# from library_forms import BookForm, AuthorForm

scriptdir = os.path.dirname(os.path.abspath(__file__))
dbfile = os.path.join(scriptdir, "library.sqlite3")

# Complete app setup and config
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'correcthorsebatterystaple'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{dbfile}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database model for IMDB movies


class Movie(db.Model):
    __tablename__ = 'Movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    age_rating = db.Column(db.String, nullable=False)
    imdb_rating = db.Column(db.String, nullable=False)


class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.Unicode, nullable=False)
    age = db.Column(db.Integer, nullable=False)


@app.get("/survey/")
def get_survey():
    # TODO create register GET route
    pass


@app.post("/survey/")
def post_survey():
    # TODO create register POST route
    pass

@app.get("/register/")
def get_register():
    # TODO create register GET route
    form = RegisterForm()
    return render_template("register.html", form=form)


@app.post("/register/")
def post_register():
    # TODO create register POST route
    pass


@app.get("/login/")
def get_login():
    # TODO create login GET route
    form = LoginForm()
    return render_template("login.html", form=form)


@app.post("/login/")
def post_login():
    # TODO create login POST route
    # login_form: LoginForm = LoginForm()
    # if login_form.validate():
    #     username: str = login_form.username.data
    #     password: str = login_form.password.data
    #     if user_db.get(username) == password:
    #         session['password'] = username
    #         return redirect(url_for("get_home"))
    #     else:
    #         flash("Invalid Username or Password")
    # else:
    #     for field, error_msg in login_form.errors.items():
    #         flash(f"{field}: {error_msg}")
    # return redirect(url_for("get_login"))
    pass


@app.route("/")
def index():
    # TODO create default route
    return redirect(url_for("get_login"))
