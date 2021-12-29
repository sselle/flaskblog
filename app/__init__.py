from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config) # gets all vars defined in the class

from app import routes