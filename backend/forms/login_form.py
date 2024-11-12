from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, ValidationError, Length
from app.models import User

def username_check(form, field):
    username = field.data
    user = User.query.filter(User.username == username).first()
    if not user:
        raise ValidationError('The username provided is not found.')
    
def password_check(form, field):
    password = field.data
    username = form.data['username']
    user = User.query.filter(User.username == username).first()
    if not user:
        raise ValidationError('User does not exist.')
    if not user.check_password(password):
        raise ValidationError('Password is incorrect.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), username_check])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=72), password_check])