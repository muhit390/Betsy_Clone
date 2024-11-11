from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, ValidationError, Length
from models.user import User


def email_in_use(form, field):
    email = field.data
    user = User.query.filter(User.email == email).first()
    if user:
        raise ValidationError("Email already in use.")


def username_in_use(form, field):
    username = field.data
    user = User.query.filter(User.username == username).first()
    if user:
        raise ValidationError("Username already in use.")


class SignUpForm(FlaskForm):
    email = StringField(
        "Email", validators=[DataRequired(), Length(max=255), email_in_use]
    )
    username = StringField(
        "Username", validators=[DataRequired(), Length(max=30), username_in_use]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=8, max=72)]
    )
    first_name = StringField(
        "First Name", validators=[DataRequired(), Length(max=255)]
    )
    last_name = StringField(
        "Last Name", validators=[DataRequired(), Length(min=8, max=255)]
    )
