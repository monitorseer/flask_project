from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=["GET", "POST"])
@login_required
def home():
    user_notes = Note.query.filter_by(user_id=current_user.id).all() # Retrieves all notes from user
    return render_template("home.html", user=current_user, notes=user_notes) # Passes notes to dashboard

@views.route('/notes', methods=["GET", "POST"])
@login_required
def notes():
    if request.method == "POST":
        title = request.form.get('title')
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        elif len(note) > 10000:
            flash('Note is too long!', category='error')
        elif len(title) > 100:
            flash('Title is too long!', category='error')
        else:
            # Adds note to DB
            new_note = Note(data=note, title=title, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("notes.html", user=current_user)

@views.route('/delete-note', methods=["POST"])
@login_required
def delete_note():
    note = json.loads(request.data) # Retrieves notes
    noteId = note['noteId'] # Loads data as a python dictionary 
    note = Note.query.get(noteId) # Looks for the note that matches the ID
    if note: # Ensures that note exists
        if note.user_id == current_user.id: # Ensures that only note creator can delete their note
            # Saves deletion into DB
            db.session.delete(note) 
            db.session.commit()

    return jsonify({}) 