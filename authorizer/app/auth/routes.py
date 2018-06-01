"""
Authentication Routes
"""

from flask import render_template, flash, redirect, url_for
from flask_login import login_user, current_user, logout_user
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, SignUpForm
from app.models import User

@bp.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('main.index'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user is None or user.check_password(form.password.data):
      flash('Invalid username or password.')
      return redirect(url_for('auth.login'))
    login_user(user, remember=form.remember_me.data)
    return redirect(url_for('main.index'))
  return render_template('auth/login.html', title="Log In", form=form)


@bp.route('/signup', methods=['GET','POST'])
def signup():
  if current_user.is_authenticated:
    return redirect(url_for('main.index'))
  form = SignUpForm()

  # if form class has a `validate_<name>` method, it will run here 
  if form.validate_on_submit():
    user = User(username=form.username.data, email=form.email.data)
    # hash password before setting
    user.set_password(form.password.data)

    # add to database
    db.session.add(user)
    db.session.commit()
    flash('Registration successful.')
    return redirect(url_for('auth.login'))
  return render_template('auth/signup.html', title="Sign Up", form=form)
  

@bp.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('main.index'))