from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models import Note, User
from . import db
from datetime import datetime
import json
import os
import requests

views = Blueprint('views', __name__)

# Main Homepage
@views.route('/', methods=["GET", "POST"])
@login_required
def home():
    user_notes = Note.query.filter_by(user_id=current_user.id).all() # Retrieves all notes from user
    return render_template("home.html", user=current_user, notes=user_notes) # Passes notes to dashboard


# Notes Page
@views.route('/notes', methods=["GET", "POST"])
@login_required
def notes():
    if request.method == "POST":
        category = request.form.get('category')
        title = request.form.get('title')
        note = request.form.get('note')
        deadline = request.form.get('deadline')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        elif len(note) > 10000:
            flash('Note is too long!', category='error')
        elif len(title) > 100:
            flash('Title is too long!', category='error')
        else:
            # Convert deadline to datetime object if it exists
            deadline_dt = None
            if deadline:
                deadline_dt = datetime.strptime(deadline, '%Y-%m-%d')
            # Adds note to DB
            new_note = Note(category=category, title=title, data=note, deadline=deadline_dt, user_id=current_user.id)
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


# Details Page
@views.route('/details')
@login_required
def details():
    user_details = User.query.filter_by(id=current_user.id).first() # Retrieves user details
    return render_template("details.html", user=current_user)


# Timetable Page
# Ensure the upload folder exists
UPLOAD_FOLDER = os.path.join('website', 'static', 'uploads') # Specifies the folder to store uploaded files
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER) # Creates folder if it doesn't exist

@views.route('/timetable', methods=["GET", "POST"])
@login_required
def timetable():
    file_path1 = None
    file_path2 = None
    if request.method == 'POST':
        # Ensures that a file is uploaded
        if 'image1' not in request.files or 'image2' not in request.files:
            flash('No file part', category='error')
            return redirect(request.url)
        
        file1 = request.files['image1']
        file2 = request.files['image2']

        for file in [file1, file2]:

            if file.filename == '':
                flash('No selected file', category='error')
                return redirect(request.url)

            # Validate file extension
            if not (file.filename.endswith('.htm') or file.filename.endswith('.html')):
                flash('Invalid file type. Please upload an .htm file.', category='error')
                return redirect(request.url)
            
            # If file exists, save it to the uploads folder
            if file:
                filename = secure_filename(file.filename) # Ensures that the filename is safe
                file_path = os.path.join(UPLOAD_FOLDER, filename) # Construct file path
                file.save(file_path) # Saves file to folder
                file_path = os.path.normpath(file_path).replace('\\', '/') # Normalize the file path and replace backslashes with forward slashes
                flash('File uploaded!', category='success')
                # Updates DB with path
                if file == file1:
                    current_user.timetable_path = file_path1
                else:
                    current_user.timetable_path1 = file_path2
                db.session.commit()
       
    if current_user.timetable_path: # Renders iframe if path exists
        file_path1 = current_user.timetable_path
        file_path2 = current_user.timetable_path1

    return render_template("timetable.html", user=current_user, file_path1=file_path1, file_path2=file_path2)


# Weather Page
@views.route('/weather')
@login_required
def weather():
    # Connects to OpenWeatherMap API for
    city_name = 'Singapore'
    API_Key = '663b69c14e4c025c11e8e8e28e7880a5'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_Key}&units=metric'

    response = requests.get(url) # Sends GET request to API
    data = response.json() # Converts response to dictionary

    # Extracts relevant data from dictionary
    longitude = data['coord']['lon']
    latitude = data['coord']['lat']
    weather = data['weather'][0]['main']
    weather_description = data['weather'][0]['description']
    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    min_temp = data['main']['temp_min']
    max_temp = data['main']['temp_max']
    pressure = data['main']['pressure']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    wind_direction = data['wind']['deg']

    # Used to display relevant data on website
    data_list = [longitude, latitude, weather, weather_description, temp, feels_like, min_temp, max_temp, pressure, humidity, wind_speed, wind_direction]

    # Connects to Data.gov.sg API for weather forecast
    sg_url = 'https://api-open.data.gov.sg/v2/real-time/api/four-day-outlook'
    sg_response = requests.get(sg_url) # Sends get request to API
    sg_data = sg_response.json() # Converts response to dictionary

    # Extracts relevant data from dictionary
    days = [forecast['day'] for forecast in sg_data['data']['records'][0]['forecasts']]
    temperature = [forecast['temperature'] for forecast in sg_data['data']['records'][0]['forecasts']]
    weather_conditions = [forecast['forecast']['text'] for forecast in sg_data['data']['records'][0]['forecasts']]
    sg_list = list(zip(days, temperature, weather_conditions))
    return render_template("weather.html", user=current_user, data=data_list, sg_data=sg_list)


# Calendar Page
@views.route('/calendar')
@login_required
def calendar():
    return render_template("calendar.html", user=current_user)


# Links Page
@views.route('/links')
@login_required
def links():
    return render_template("links.html", user=current_user)