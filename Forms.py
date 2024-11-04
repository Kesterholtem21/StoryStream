from flask_wtf import FlaskForm
from wtforms.fields import StringField, IntegerField, SubmitField, SelectField, EmailField
from wtforms.validators import InputRequired, Optional, Length, Email


class RegisterForm():
    #TODO fill this out
    email = EmailField("Email: ", validators=[Email()])
    username = StringField("Username", validators=[InputRequired()])
    password = StringField("Password", validators=[InputRequired(), Length(min=8, max=12)])
    pass

class LoginForm():
    #TODO fill this out
    email = EmailField("Email: ", validators=[Email()])
    username = StringField("Username", validators=[InputRequired()])
    password = StringField("Password", validators=[InputRequired(), Length(min=8, max=12)])
    pass

class PreferenceForm():
    #TODO fill this out
    pass