from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


# For users to log into their accounts
@auth.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Extracts user info from form
        email = request.form.get('email')
        password = request.form.get('password')

        # Queries DB for user matching sent email
        user = User.query.filter_by(email=email).first()

        # Verification of user
        if user:
            if check_password_hash(user.password, password):
                # Correct password
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True) # Conveniences the user to be able to stay logged in
                return redirect(url_for('views.home'))
            else:
                # Wrong password
                flash('Incorrect password, try again.', category='error')
        else:
            # Unregistered email
            flash('Email does not exist.', category='error')
    return render_template('login.html', user=current_user)


# For users to create new accounts
@auth.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Extracts user info from form
        name = request.form.get('name')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Queries DB for user matching sent email
        user = User.query.filter_by(email=email).first()

        # Validation with flashes
        if user:
            flash('Email already exists.', category='error')
        elif len(name) < 2:
            flash('Name must be minimally 2 letters long.', category='error')
        elif len(name) > 100:
            flash('Name is too long.', category='error')
        elif len(email) > 100:
            flash('Email is too long.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be minimally 7 characters long.', category='error')
        elif len(password1) > 128:
            flash('Password must be at most 128 characters long!', category='error')
        else:
            # Associates a DB object with the new user, also hashes and salts the password for extra security
            new_user = User(email=email, name=name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
        
    # GET requests just loads the register template
    return render_template('register.html', user=current_user)


# For users to log out of their accounts
@auth.route('/logout')
@login_required # Ensures that page can only be accessed by logged in users
def logout():
    logout_user()
    return redirect(url_for('auth.login'))