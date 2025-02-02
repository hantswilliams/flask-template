from flask_wtf.file import FileAllowed
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, PasswordField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from app.models import BaseUser


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = BaseUser.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = BaseUser.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = BaseUser.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = BaseUser.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class AdminCreateRoleForm(FlaskForm):
    role = StringField('Role', validators=[DataRequired()])
    submit = SubmitField('Create Role')

class AdminSetPermissionsForm(FlaskForm):
    user = SelectField('User', validators=[DataRequired()], choices=[])  # SelectField for users
    endpoint = SelectField('API Endpoint', validators=[DataRequired()], choices=[])  # SelectField for API endpoints
    role = SelectField('Role', validators=[DataRequired()], choices=[])  # SelectField for roles
    can_read = BooleanField('Read')
    can_write = BooleanField('Write')
    can_update = BooleanField('Update')
    can_delete = BooleanField('Delete')
    submit = SubmitField('Set Permissions')
