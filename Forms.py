from flask_wtf import FlaskForm
from wtforms.fields import StringField, IntegerField, SubmitField, SelectField, EmailField
from wtforms.validators import InputRequired, Optional, Length, Email


class RegisterForm(FlaskForm):
    # TODO fill this out
    email = EmailField("Email: ", validators=[Email()])
    username = StringField("Username", validators=[InputRequired()])
    password = StringField("Password", validators=[InputRequired(), Length(min=8, max=12)])


class LoginForm(FlaskForm):
    # TODO fill this out
    email = EmailField("Email: ", validators=[Email()])
    username = StringField("Username", validators=[InputRequired()])
    password = StringField("Password", validators=[InputRequired(), Length(min=8, max=12)])
    submit = SubmitField("Login")


class PreferenceForm(FlaskForm):
    # TODO fill this out
    pass
