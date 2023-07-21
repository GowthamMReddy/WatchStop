from flask import Blueprint
from flask import render_template, redirect, request, flash, url_for, current_app
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

