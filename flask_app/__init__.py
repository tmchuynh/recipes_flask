# __init__.py
from flask import Flask
app = Flask(__name__)
app.secret_key = "never gonna move to texas, come to california"
DATABASE = "recipe"