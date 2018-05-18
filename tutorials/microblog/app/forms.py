"""Forms management module

Various classes for all forms used in the application

"""
from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User



class LoginForm(FlaskForm):
  """Build form for logging in to app. Subclass FlaskForm from Flask-WTF."""
  username = StringField(_l('Username'), validators=[DataRequired()])
  password = PasswordField(_l('Password'), validators=[DataRequired()])
  remember_me = BooleanField(_l('Remember Me'))
  submit = SubmitField(_l('Sign In'))



class RegistrationForm(FlaskForm):
  """Build form for registering on to app. Subclass FlaskForm from Flask-WTF"""
  username = StringField(_l('Username'), validators=[DataRequired()])
  email = StringField(_l('Email'), validators=[DataRequired(), Email()])
  password = PasswordField(_l('Password'), validators=[DataRequired()])
  password2 = PasswordField(_l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField(_l('Register'))

  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user is not None:
      raise ValidationError(_l('Please use a different username.'))

  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user is not None:
      raise ValidationError(_l('Please use a different email address.'))



class EditProfileForm(FlaskForm):
  """Build form for editing profile information. Subclass FlaskForm from Flask-WTF"""
  username = StringField(_l('Username'), validators=[DataRequired()])
  about_me = TextAreaField(_l('About Me'), validators=[Length(min=0,max=140)])
  submit = SubmitField(_l('Submit'))

  def __init__(self, original_username, *args, **kwargs):
    super(EditProfileForm, self).__init__(*args, **kwargs)
    self.original_username = original_username
  
  def validate_username(self, username):
    if username.data != self.original_username:
      user = User.query.filter_by(username = self.username.data).first()
      if user is not None:
        raise ValidationError(_l('Please select a different username.'))



class PostForm(FlaskForm):
  """Build generic form for posting text. Subclass FlaskForm from Flask-WTF"""
  post = TextAreaField(
    _l('Say something'),
    validators=[DataRequired(), Length(min=1, max=140)])
  submit = SubmitField(_l('Submit'))



class ResetPasswordRequestForm(FlaskForm):
  """Build form for requesting a password reset"""
  email = StringField(_l('Email'), validators=[DataRequired(), Email()])
  submit = SubmitField(_l('Request Password Reset'))



class ResetPasswordForm(FlaskForm):
  """Build form to reset password"""
  password = PasswordField(_l('Password'), validators=[DataRequired()])
  password2 = PasswordField(_l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField(_l('Request Password Reset'))