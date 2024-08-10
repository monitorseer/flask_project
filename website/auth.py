from flask import Blueprint, render_template, request, redirect, url_for


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=["GET", "POST"])
def login():
    return render_template('login.html')