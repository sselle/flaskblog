# first app = the module 
# second app = instance of Flask created in __init__.py
from app import app

@app.route('/')
@app.route('/index')
def index():
    return 'hello world!'