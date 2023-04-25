from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, Email, EqualTo
from wtforms.fields import FileField
from flask_wtf.file import FileRequired, FileAllowed
from flask_wtf import CSRFProtect
from app import app
from app.models import User


csrf = CSRFProtect(app)



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class FindPersonForm(FlaskForm):
    person = StringField('Whom are you looking for?', validators=[DataRequired(), Length(3, 50)])
    submit = SubmitField('Submit')


class AddPersonForm(FlaskForm):
    group = StringField(label='Enter group', validators=[DataRequired()])
    name = StringField(label='Enter name', validators=[DataRequired(), Length(3, 50)])
    mobile = StringField(label='Enter mobile', validators=[DataRequired(), Length(9, 10)])
    nationality = StringField(label='Enter nationality', validators=[DataRequired(), Length(3, 50)])
    department = StringField(label='Enter department')
    position = StringField(label='Enter position', validators=[DataRequired()])
    team = StringField(label='Enter team', validators=[Length(3, 20)])
    sport = StringField(label='Enter sport', validators=[Length(3, 20)])
    image = FileField(validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'], 'JPG, JPEG or PNG Images only!')])
    submit = SubmitField('Submit')

