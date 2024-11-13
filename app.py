###############################################################################
# Imports
###############################################################################
from __future__ import annotations
from flask import Flask, request, render_template, redirect, url_for, abort, session
from flask import flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_required
from flask_login import login_user, logout_user, current_user
from Forms import RegisterForm, LoginForm, PreferenceForm, SearchForm
from Hasher import UpdatedHasher

# make sure the script's directory is in Python's import path
# this is only required when run from a different directory
import os
import sys


###############################################################################
# Basic Configuration
###############################################################################

# Identify necessary files

script_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(script_dir)
# once script directory is in path, import Contact and ContactForm
# from library_forms import BookForm, AuthorForm

scriptdir = os.path.dirname(os.path.abspath(__file__))
dbfile = os.path.join(scriptdir, "library.sqlite3")
pepfile = os.path.join(scriptdir, "pepper.bin")

# open and read the contents of the pepper file into your pepper key
# NOTE: you should really generate your own and not use the one from the starter
with open(pepfile, 'rb') as fin:
    pepper_key = fin.read()

# create a new instance of UpdatedHasher using that pepper key
pwd_hasher = UpdatedHasher(pepper_key)

# Complete app setup and config
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'correcthorsebatterystaple'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{dbfile}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Prepare and connect the LoginManager to this app
login_manager = LoginManager()
login_manager.init_app(app)
# function name of the route that has the login form (so it can redirect users)
login_manager.login_view = 'get_login'  # type: ignore
login_manager.session_protection = "strong"
# function that takes a user id and


@login_manager.user_loader
def load_user(uid: int) -> User | None:
    return User.query.get(int(uid))


###############################################################################
# Database Setup
###############################################################################

# Database model for IMDB movies


class Movie(db.Model):
    __tablename__ = 'Movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    age_rating = db.Column(db.String, nullable=False)
    imdb_rating = db.Column(db.String, nullable=False)


class Book(db.Model):
    __tablename__ = 'Books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)


class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    passwordHash = db.Column(db.Unicode, nullable=False)

    # make a write-only password property that just updates the stored hash
    @property
    def password(self):
        raise AttributeError("password is a write-only attribute")

    @password.setter
    def password(self, pwd: str) -> None:
        self.passwordHash = pwd_hasher.hash(pwd)

    # add a verify_password convenience method
    def verify_password(self, pwd: str) -> bool:
        return pwd_hasher.check(pwd, self.passwordHash)


###############################################################################
# Route Handlers
###############################################################################
with app.app_context():
    db.create_all()


@app.get("/viewed/")
def get_viewed():
    # TODO create register GET route
    return render_template("viewedPage.html")


@app.post("/viewed/")
def post_viewed():
    # TODO create register POST route
    pass


@app.get("/home/")
def get_home():
    form = SearchForm()
    search_results = []
    return render_template("homePage.html", form=form, search_results=search_results, current_user=current_user)


@app.post("/home/")
def post_home():
    form = SearchForm()
    search_results = []

    if form.validate_on_submit():
        search_term = form.searchTerm.data.strip()
        movie_results = Movie.query.filter(
            Movie.title.ilike(f"%{search_term}%")).all()
        book_results = Book.query.filter(
            Book.title.ilike(f"%{search_term}%")).all()
        search_results.extend(movie_results + book_results)

    return render_template("homePage.html", form=form, search_results=search_results, current_user=current_user)


@app.get("/favorites/")
def get_favorites():
    # TODO create register GET route
    movies = Movie.query.all()  # TODO: Load the list of all pets from the database
    return render_template("favoritesPage.html", movies=movies)


@app.post("/favorites/")
def post_favorites():
    # TODO create register POST route
    pass


@app.get("/profile/")
def get_profile():
    # TODO create register GET route
    return render_template("profilePage.html")


@app.post("/profile/")
def post_profile():
    # TODO create register POST route
    pass


@app.get("/survey/")
def get_survey():
    # TODO create register GET route
    form = PreferenceForm()
    return render_template("survey.html", form=form)


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
    form = RegisterForm()
    if form.validate():
        # check if there is already a user with this email address
        user = User.query.filter_by(username=form.username.data).first()
        # if the email address is free and passwords match, create a new user and send to login
        if user is None:
            if form.password.data == form.confirmPassword.data:
                user = User(username=form.username.data,
                            password=form.password.data, age=form.age.data)  # type:ignore
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('get_login'))
            else:
                flash('Make sure your passwords match')
                return redirect(url_for('get_register'))
        else:  # if the user already exists
            # flash a warning message and redirect to get registration form
            flash('That username is already taken')
            return redirect(url_for('get_register'))
    else:  # if the form was invalid
        # flash error messages and redirect to get registration form again
        for field, error in form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('get_register'))


@app.get("/login/")
def get_login():
    # create login GET route
    form = LoginForm()
    return render_template("login.html", form=form)


@app.post("/login/")
def post_login():
    form = LoginForm()
    if form.validate():
        # try to get the user associated with this email address
        user = User.query.filter_by(username=form.username.data).first()
        # if this user exists and the password matches
        if user is not None and user.verify_password(form.password.data):
            # log this user in through the login_manager
            login_user(user)
            # redirect the user to the page they wanted or the home page
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('get_home')
            return redirect(next)
        else:  # if the user does not exist or the password is incorrect
            # flash an error message and redirect to login form
            flash('Invalid email address or password')
            return redirect(url_for('get_login'))
    else:  # if the form was invalid
        # flash error messages and redirect to get login form again
        for field, error in form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('get_login'))


@app.route("/")
def index():
    # TODO create default route
    return redirect(url_for("get_login"))


@app.get('/logout/')
@login_required
def get_logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('index'))
