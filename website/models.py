from . import db # Imports db from __init__ file in same folder
from flask_login import UserMixin

# Stores informaton about user
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True) # Only one user can have one email at a time
    password = db.Column(db.String(128))