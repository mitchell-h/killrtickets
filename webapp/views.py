from webapp import webapp
from flask import render_template

@webapp.route('/')
@webapp.route('/index')
def index():
    return "Hello, World!"

@webapp.route('/test')
def test():
    user = {'nickname': 'mitch'}  # fake user
    return render_template('test.html', user=user)
