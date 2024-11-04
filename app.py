from flask import Flask, request, render_template, redirect, url_for, abort
from flask import flash
from flask_sqlalchemy import SQLAlchemy

# make sure the script's directory is in Python's import path
# this is only required when run from a different directory
import os, sys
script_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(script_dir)
# once script directory is in path, import Contact and ContactForm
from Forms import LoginForm, RegisterForm, PreferenceForm

scriptdir = os.path.dirname(os.path.abspath(__file__))
dbfile = os.path.join(scriptdir, "StoryStream.sqlite3")

# Complete app setup and config
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
#app.config['SECRET_KEY'] = 'correcthorsebatterystaple'
app.config['SECRET_KEY'] = 'totallysecretimportantstring'
# TODO: connect your app to a SQLite database



app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{dbfile}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)



@app.get("/servey/")
def get_servey():
    #create servey GET route
    form = PreferenceForm()
    return render_template("servey.html", form=form)

@app.post("/servey/")
def post_servey():
    #TODO create servey POST route
    pass

@app.get("/register/")
def get_register():
    #TODO create register GET route
    form = RegisterForm()
    return render_template("register.html", form=form)

@app.post("/register/")
def post_register():
    #TODO create register POST route
    pass

@app.get("/login/")
def get_login():
    #TODO create login GET route
    form = LoginForm()
    return render_template("login.html", form=form)

@app.post("/login/")
def post_login():
    #TODO create login POST route
    pass


@app.route("/")
def index():
    #TODO create default route
    return redirect(url_for("get_login"))
    pass