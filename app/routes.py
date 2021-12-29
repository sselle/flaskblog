# first app = the module 
# second app = instance of Flask created in __init__.py
from flask import render_template, flash, redirect
from flask.helpers import url_for
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    # fake user 'db'
    user = {'username': 'Sven'}
    # fake posts 'db'
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Nice day in NBG'
        },
        {
            'author': {'username': 'Alice'},
            'body': 'It is sunny outside'
        },
    ]
    return render_template('index.html', title='Home', 
                            user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login requested for user {form.username.data}, remember_me={form.remember_me.data}')
        return redirect( url_for('index'))
    return render_template('login.html', title='Sign in', form=form)