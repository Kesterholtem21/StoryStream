###############################################################################
# Imports
###############################################################################
from __future__ import annotations
from flask import Flask, request, render_template, redirect, url_for, abort, session, jsonify
from flask import flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask_login import UserMixin, LoginManager, login_required
from flask_login import login_user, logout_user, current_user
from Forms import RegisterForm, LoginForm, PreferenceForm, SearchForm
from Hasher import UpdatedHasher
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm.exc import NoResultFound
import requests
from datetime import datetime, UTC

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

# many-to-many relationship tables
user_book_favorites = db.Table(
    'user_book_favorites',
    db.Column('user_id', db.Integer, db.ForeignKey(
        'Users.id'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey(
        'Books.id'), primary_key=True)
)

user_movie_favorites = db.Table(
    'user_movie_favorites',
    db.Column('user_id', db.Integer, db.ForeignKey(
        'Users.id'), primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey(
        'Movies.id'), primary_key=True)
)

# Database for comments


class BookComment(db.Model):
    __tablename__ = "BookComments"
    commentID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('Users.id'))
    bookID = db.Column(db.Integer, db.ForeignKey('Books.id'))
    text = db.Column(db.String, nullable=False)


class MovieComment(db.Model):
    __tablename__ = "MovieComments"
    commentID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('Users.id'))
    movieID = db.Column(db.Integer, db.ForeignKey('Movies.id'))
    text = db.Column(db.String, nullable=False)

# Database model for IMDB movies


class Movie(db.Model):
    __tablename__ = 'Movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.String, nullable=True)
    poster_path = db.Column(db.String, nullable=True)
    # genre = db.Column(db.String, nullable=False)
    # age_rating = db.Column(db.String, nullable=False)
    # imdb_rating = db.Column(db.String, nullable=False)


class Genres(db.Model):
    __tablename__ = 'Genres'
    id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String, nullable=False)


movie_genres = db.Table(
    'movie_genre',
    db.Column('movies_id', db.Integer, db.ForeignKey(
        'Movies.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey(
        'Genres.id'), primary_key=True)
)


class Book(db.Model):
    __tablename__ = 'Books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    poster_path = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)


class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    passwordHash = db.Column(db.Unicode, nullable=False)
    isAdmin = db.Column(db.Integer, nullable=False)
    firstTimeLoggedIn = db.Column(db.Integer, nullable=False)
    genres = db.Column(db.Unicode, nullable=False)
    book_favorites = db.relationship(
        'Book', secondary=user_book_favorites, backref='users')
    movie_favorites = db.relationship(
        'Movie', secondary=user_movie_favorites, backref='users')

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
    db.create_all()  # SQLAlchemy should create them in the correct order now


@app.get("/get_Book_comments")
def get_Book_comments():

    try:
        bookComments = BookComment.query.all()

        commentList = [
            {
                "userID": comment.userID,
                "itemID": comment.bookID,
                "text": comment.text,
                # "timestamp" : datetime.now(UTC).isoformat(),
                "type":   "Book"
            }
            for comment in bookComments
        ]

        # print((commentList))
        return jsonify({"success": True, "commentList": commentList}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.get("/get_Movie_comments")
def get_Movie_comments():

    try:
        movieComments = MovieComment.query.all()

        commentList = [
            {
                "userID": comment.userID,
                "itemID": comment.movieID,
                "text": comment.text,
                "timestamp": datetime.now(UTC).isoformat(),
                "type":   "Movie"
            }
            for comment in movieComments
        ]

        # print((commentList))
        return jsonify({"success": True, "commentList": commentList}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
@app.get("/get_User_comments/<int:userID>")
def get_User_comments(userID):
    try:
        moviecomments = MovieComment.query.filter_by(userID=userID).all()
        bookcomments = BookComment.query.filter_by(userID=userID).all()

        commentList = [
            {
                "userID": comment.userID,
                "itemID": comment.movieID,
                "text": comment.text,
                "timestamp": datetime.now(UTC).isoformat(),
                "type": "Movie",
                "commentID" :  comment.commentID
            }
            for comment in moviecomments
        ] + [
            {
                "userID": comment.userID,
                "itemID": comment.bookID,
                "text": comment.text,
                "type": "Book",
                "commentID" :   comment.commentID
            }
            for comment in bookcomments
        ]

        return jsonify({"success": True, "commentList": commentList}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500



@app.post("/post_comments")
def post_comments():

    data = request.get_json()
    user_id = data.get("user_id")
    item_id = data.get("itemId")
    text = data.get("text")
    type = data.get("type")

    print(type)

    try:
        if type == "Book":
            # add new comment to book table
            comment = BookComment(userID=int(user_id),
                                  bookID=int(item_id), text=text)
            db.session.add(comment)
            db.session.commit()

        if type == "Movie":
            # add new comment to movie table
            comment = MovieComment(userID=int(
                user_id), movieID=int(item_id), text=text)
            db.session.add(comment)
            db.session.commit()

        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False}), 500


@app.get("/admin/")
def get_admin():

    if current_user.isAdmin:
        form = SearchForm()
        searchResults = []

        listOfUsers = User.query.all()
        for user in listOfUsers:
            print(user.id)

        return render_template("AdminPage.html", users=listOfUsers, form=form, searchResults=searchResults)
    return redirect(url_for("get_home"))


@app.post("/change_admin/")
def change_admin():

    if not current_user.is_authenticated:
        return jsonify({"error": "User not logged in"}), 401

    data = request.get_json()
    item_id = data.get("id")
    item_type = data.get("type")
    try:
        if item_type == "user":
            user = User.query.get(item_id)
            if user.isAdmin:
                user.isAdmin = False
            else:
                user.isAdmin = True

        db.session.commit()
        return jsonify({"success": True}), 200

    except (SQLAlchemyError, NoResultFound) as e:
        db.session.rollback()
        print(e)
        return jsonify({"error": "An error occurred"}), 500


@app.post("/admin/")
@login_required
def post_admin():
    form = SearchForm()
    user_results = []

    if form.validate_on_submit():
        search_term = form.searchTerm.data.strip()
        user_results = User.query.filter(
            User.username.ilike(f"%{search_term}%")).all()

        return render_template("AdminPage.html", form=form, user_results=user_results, user=current_user)

@app.post("/deleteComment/")
def delete_Comment():
    data = request.get_json()
    type = data.get("type")
    commentID = data.get("commentID")
    print(commentID)
    print(type)
    if type == "Book":
        commentToRemove = BookComment.query.filter(BookComment.commentID == int(commentID)).first()
        print(commentToRemove)
        db.session.delete(commentToRemove)
        db.session.commit()
    if type == "Movie":
        commentToRemove = MovieComment.query.filter(MovieComment.commentID == int(commentID)).first()
        print(commentToRemove)
        db.session.delete(commentToRemove)
        db.session.commit()
    return jsonify({"success": True}), 200
    

@app.post("/remove_user/")
def remove_user():
    data = request.get_json()
    userId = data.get("id")
    userToRemove = User.query.filter(User.id == userId).first()
    usersComments = BookComment.query.filter(BookComment.userID == userId).all() + MovieComment.query.filter(MovieComment.userID == userId).all()
    for comment in usersComments:
        db.session.delete(comment)
    db.session.delete(userToRemove)

    db.session.commit()
    return jsonify({"success": True}), 200



@app.get("/viewed/")
@login_required
def get_viewed():
    # TODO create register GET route

    genres = current_user.genres
    print(genres)
    if genres:
        book_results = Book.query.filter(
            Book.genre.ilike(f"%{genres[0]}%")).all()
        book_results = book_results + \
            Book.query.filter(Book.genre.ilike(f"%{genres[1]}%")).all()
        book_results = book_results + \
            Book.query.filter(Book.genre.ilike(f"%{genres[2]}%")).all()

        movie_api_results = fetch_tmdb_genre(genres)
        if movie_api_results:
            movie_results = movie_api_results
        return render_template("viewedPage.html", user=current_user, movie_results=movie_results, book_results=book_results)
    else:
        movie_results = []
        book_results = []

        return render_template("viewedPage.html", user=current_user, movie_results=movie_results, book_results=book_results)


def fetch_tmdb_genre(genres):
    api_key = 'e0b0133a262a178bcb578be381618ef7'
    movie_results = []

    for genre in genres:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={
            api_key}&query={genre}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                movie_results.extend(data.get("results", []))
            else:
                print("Failed to fetch TMDb data")
        except requests.RequestException as e:
            print("Error")

    return movie_results


@app.post("/viewed/")
def post_viewed():
    pass


@app.get("/home/")
@login_required
def get_home():
    form = SearchForm()
    search_results = []
    return render_template("homePage.html", form=form, search_results=search_results, current_user=current_user)


@app.post("/home/")
@login_required
def post_home():
    form = SearchForm()
    book_results = []
    movie_results = []

    if form.validate_on_submit():
        search_term = form.searchTerm.data.strip()

        book_results = Book.query.filter(
            or_(
                Book.title.ilike(f"%{search_term}%"),
                Book.author.ilike(f"%{search_term}%")
            )
        ).all()

        # Fetch data from TMDb API for movies
        movie_api_results = fetch_tmdb_movies(search_term)
        if movie_api_results:
            movie_results = movie_api_results

    return render_template("homePage.html", form=form, movie_results=movie_results,
                           book_results=book_results, current_user=current_user)


def fetch_tmdb_movies(query):
    api_key = 'e0b0133a262a178bcb578be381618ef7'
    url = f"https://api.themoviedb.org/3/search/movie?api_key={
        api_key}&query={query}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("results", [])
        else:
            print(f"Failed to fetch TMDb data: {response.status_code}")
            return []
    except requests.RequestException as e:
        print(f"Error during API call: {e}")
        return []


def fetch_movie_by_id(movie_id):
    api_key = 'e0b0133a262a178bcb578be381618ef7'
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Failed to fetch TMDb data: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error during API call: {e}")
        return None


@app.post("/add_favorite")
@login_required
def add_favorite():

    data = request.get_json()
    item_id = data.get("id")
    item_type = data.get("type")

    try:
        if item_type == "book":
            book = Book.query.get(item_id)
            if book and book not in current_user.book_favorites:
                current_user.book_favorites.append(book)

        elif item_type == "movie":
            movie_data = fetch_movie_by_id(item_id)
            movie = Movie.query.filter_by(id=item_id).first()
            if not movie:
                movie = Movie(
                    id=movie_data['id'],
                    title=movie_data['title'],
                    poster_path=movie_data['poster_path']
                )
            if movie and movie not in current_user.movie_favorites:
                current_user.movie_favorites.append(movie)

        db.session.commit()
        return redirect(url_for('get_home'))

    except (SQLAlchemyError, NoResultFound) as e:
        db.session.rollback()
        print(e)
        flash("An error occurred while adding to favorites.", "error")
        return redirect(url_for('get_home'))


@app.post("/remove_favorite")
@login_required
def remove_favorite():
    data = request.get_json()
    item_id = data.get("id")
    item_type = data.get("type")

    try:
        if item_type == "book":
            book = Book.query.get(item_id)
            if book and book in current_user.book_favorites:
                current_user.book_favorites.remove(book)

        elif item_type == "movie":
            movie = Movie.query.filter_by(id=item_id).first()
            if movie and movie in current_user.movie_favorites:
                current_user.movie_favorites.remove(movie)

        db.session.commit()
        return redirect(url_for('get_home'))

    except (SQLAlchemyError, NoResultFound) as e:
        db.session.rollback()
        print(e)
        flash("An error occurred while removing from favorites.", "error")
        return redirect(url_for('get_home'))


@app.get("/favorites/")
@login_required
def get_favorites():
    fav_books = current_user.book_favorites
    fav_movies = current_user.movie_favorites
    print(fav_books)
    print(fav_movies)
    return render_template("favoritesPage.html", current_user=current_user, movies=fav_movies, books=fav_books)


@app.post("/favorites/")
@login_required
def post_favorites():
    # TODO create register POST route
    pass


@app.get("/profile/")
@login_required
def get_profile():
    # TODO create register GET route
    return render_template("profilePage.html", user=current_user)


@app.post("/profile/")
@login_required
def post_profile():
    # TODO create register POST route
    pass


@app.get("/survey/")
@login_required
def get_survey():
    # TODO create register GET route
    form = PreferenceForm()
    if current_user.firstTimeLoggedIn == 0:
        current_user.firstTimeLoggedIn = 1
        db.session.commit()
    return render_template("survey.html", form=form, user=current_user)


@app.post("/survey/")
@login_required
def post_survey():
    form = PreferenceForm()

    if form.validate():
        genre1 = form.genre1.data

        genre2 = form.genre2.data

        genre3 = form.genre3.data

        genres = genre1 + "," + genre2 + "," + genre3

        current_user.genres = genres
        db.session.commit()
        print(current_user.genres)

        return redirect(url_for("get_viewed"))
    return redirect(url_for("get_survey"))


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
                            password=form.password.data, age=form.age.data, isAdmin=0,firstTimeLoggedIn=0 ,genres="")  # type:ignore
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
                if current_user.firstTimeLoggedIn == 0:
                    next = url_for('get_survey')
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
