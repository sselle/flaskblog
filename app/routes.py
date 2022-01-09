from datetime import datetime

from flask import render_template, flash, redirect, request
from flask.helpers import url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_fix, url_parse
from wtforms.validators import Email

from app import app # first app = the module, second app = instance of Flask created in __init__.py
from app import db
from app.forms import LoginForm, RegisterForm, EditProfileForm, EmptyForm
from app.models import User

@app.route('/')
@app.route('/index')
@login_required
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
    return render_template('index.html', title='Home', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect( url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect( url_for('login'))
        # check succesful, login user
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        # werkzeug url_parse to prevent attacks by routing to another URL through next
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
        flash(f'Login requested for user {form.username.data}, remember_me={form.remember_me.data}')
        return redirect( url_for('index'))
    return render_template('login.html', title='Sign in', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect( url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Congrats, you are now registered as {form.username.data}')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>') #username var is passed into function below decorator
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts, form=form)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
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
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


# executed right before ANY view function in the app
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit() #db.session.add is done internally by flask when using current_user

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))