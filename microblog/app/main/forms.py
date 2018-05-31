"""
User Forms
"""

from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Length
from app.models import User


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
  post = TextAreaField(_l('Say something'), validators=[DataRequired(), Length(min=1, max=140)])
  submit = SubmitField(_l('Submit'))