from flask_wtf import FlaskForm
from wtforms.fields import StringField, IntegerField, SubmitField, SelectField, EmailField, SelectMultipleField, PasswordField
from wtforms.validators import InputRequired, Optional, Length, Email


class RegisterForm(FlaskForm):
    # TODO fill this out
    username = StringField("Username", validators=[InputRequired()])
    password = StringField("Password", validators=[
                           InputRequired(), Length(min=8, max=12)])
    confirmPassword = StringField("Confirm Password", validators=[
                                  InputRequired(), Length(min=8, max=12)])
    age = IntegerField("Age: ", validators=[InputRequired()])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    # TODO fill this out
    username = StringField("Username", validators=[InputRequired()])
    password = StringField("Password", validators=[
                           InputRequired(), Length(min=8, max=12)])
    submit = SubmitField("Login")


class PreferenceForm(FlaskForm):
    # TODO fill this out
    genre1 = SelectField(
        "Pick a Genre YOU like: ", validators=[], choices=["Romance", "Science Fiction", "Mystery", "Horror", "Historical Fiction", "Fantasy", "Adventure", "Thriller", "Fiction", "Non Fiction"])
    genre2 = SelectField(
        "Pick a Genre YOU like: ", validators=[], choices=["Romance", "Science Fiction", "Mystery", "Horror", "Historical Fiction", "Fantasy", "Adventure", "Thriller", "Fiction", "Non Fiction"])
    genre3 = SelectField(
        "Pick a Genre YOU like: ", validators=[], choices=["Romance", "Science Fiction", "Mystery", "Horror", "Historical Fiction", "Fantasy", "Adventure", "Thriller", "Fiction", "Non Fiction"])
    submit = SubmitField("Submit")

class SearchForm(FlaskForm):
    searchTerm = StringField("Search", validators=[Optional()])
    submit = SubmitField("Submit")
