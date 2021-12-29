# first app = the module 
# second app = instance of Flask created in __init__.py
from flask import render_template
from app import app

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