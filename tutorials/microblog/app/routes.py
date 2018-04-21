from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
  user = {'username': 'Zach'}
  posts = [
    {
      "author": {"username": "John"},
      "body": "A simple test post"
    },
    {
      "author": {"username": "Peter"},
      "body": "Flask is awesome"
    },
  ]
  return render_template('index.html', title='Home', user=user, posts=posts)