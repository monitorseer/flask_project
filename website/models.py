from . import db # Imports db from __init__ file in same folder
from flask_login import UserMixin
from sqlalchemy import func


# Stores information about notes
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100)) # Specifies whether it is Note or Work Reminder
    title = db.Column(db.String(100))
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now()) # Timezone is based on user's timezone
    deadline = db.Column(db.DateTime(timezone=True), nullable=True) # Stores deadline for note
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # Connects note to user

# Stores informaton about user
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True) # Only one user can have one email at a time
    password = db.Column(db.String(128))
    timetable_path = db.Column(db.String(150), nullable=True) # Stores path to timetable
    timetable_path1 = db.Column(db.String(150), nullable=True) # Stores path to timetable
    notes = db.relationship('Note') # Connects user to notes