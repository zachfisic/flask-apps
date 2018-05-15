"""Routing logic for URLs

Determines action for paths taken in app.
Utilizes decorators to associate a callback function to a route or set of routes.

"""
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.models import User, Post
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, ResetPasswordRequestForm, ResetPasswordForm
from app.email import send_password_reset_email


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
  """Handle index page logic"""
  form = PostForm()
  if form.validate_on_submit():
    post = Post(body=form.post.data, author=current_user)
    db.session.add(post)
    db.session.commit()
    flash('Post added.')
    return redirect(url_for('index'))
  # handle pagination
  page = request.args.get('page', 1, type=int)
  posts = current_user.followed_posts().paginate(page, app.config['POSTS_PER_PAGE'], False)
  next_url = url_for('index', page=posts.next_num) if posts.has_next else None
  prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None
  
  return render_template('index.html', title='Home', posts=posts.items, form=form, next_url=next_url, prev_url=prev_url)



@app.route('/login', methods=['GET', 'POST'])
def login():
  """Log user in"""
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user is None or not user.check_password(form.password.data):
      flash('Invalid username or password')
      return redirect(url_for('login'))
    # sets current_user once logged in
    login_user(user, remember=form.remember_me.data)
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
      next_page = url_for('index')
    return redirect(next_page)
  return render_template('login.html', title='Sign In', form=form)



@app.route('/logout')
def logout():
  """Log user out"""
  logout_user()
  return redirect(url_for('index'))



@app.route('/register', methods=['GET', 'POST'])
def register():
  """Register user to app"""
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(username=form.username.data, email=form.email.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    flash('You have been registered.')
    return redirect(url_for('login'))
  return render_template('register.html', title='Register', form=form)



@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
  """Handle user request for password reset"""
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = ResetPasswordRequestForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user:
      send_password_reset_email(user)
    flash('Check your email for the instructions to reset your password')
    return redirect(url_for('login'))
  return render_template('reset_password_request.html', title='Reset Password', form=form)



@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
  """Reset password"""
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  user = User.verify_reset_password_token(token)
  if not user:
    return redirect(url_for('index'))
  form = ResetPasswordForm()
  if form.validate_on_submit():
    user.set_password(form.password.data)
    db.session.commit()
    flash('Password has been reset')
    return redirect(url_for('login'))
  return render_template('reset_password.html', form=form)



@app.route('/user/<username>')
@login_required
def user(username):
  """Display user given by route param"""
  user = User.query.filter_by(username=username).first_or_404()
  page = request.args.get('page', 1, type=int)
  posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
  next_url = url_for('user', username=user.username, page=posts.next_num) if posts.has_next else None
  prev_url = url_for('user', username=user.username, page=posts.prev_num) if posts.has_prev else None

  return render_template('user.html', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)



@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
  """Allow user to edit profile"""
  # the profile form must validate a potential username change
  form = EditProfileForm(current_user.username)
  if form.validate_on_submit():
    current_user.username = form.username.data
    current_user.about_me = form.about_me.data
    db.session.commit()
    flash('Your changes have been saved.')
    return redirect(url_for('edit_profile'))
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.about_me.data = current_user.about_me
  return render_template('edit_profile.html', title="Edit Profile", form=form)



@app.before_request
def before_request():
  """Execute some logic before the app makes any request"""
  if current_user.is_authenticated:
    current_user.last_seen = datetime.utcnow()
    db.session.commit()



@app.route('/follow/<username>')
@login_required
def follow(username):
  """Follow a user given by a route param"""
  user = User.query.filter_by(username=username).first()
  if user is None:
    flash('User {} not found.'.format(username))
    return redirect(url_for('index'))
  if user == current_user:
    flash('You cannot follow yourself.')
    return redirect(url_for('user', username=username))
  current_user.follow(user)
  db.session.commit()
  flash('Following {}'.format(username))
  return redirect(url_for('user', username=username))



@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
  """Unfollow a user given by a route param"""
  user = User.query.filter_by(username=username).first()
  if user is None:
    flash('User {} not found.'.format(username))
    return redirect(url_for('index'))
  if user == current_user:
    flash('You cannot unfollow yourself.')
    return redirect(url_for('user', username=username))
  current_user.unfollow(user)
  db.session.commit()
  flash('Following {}'.format(username))
  return redirect(url_for('user', username=username))



@app.route('/explore')
@login_required
def explore():
  """Handle explore page logic"""
  # handle pagination
  page = request.args.get('page', 1, type=int)
  posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
  next_url = url_for('explore', page=posts.next_num) if posts.has_next else None
  prev_url = url_for('explore', page=posts.prev_num) if posts.has_prev else None
  
  return render_template('index.html', title='Explore', posts=posts.items, next_url=next_url, prev_url=prev_url)