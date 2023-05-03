from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from .models import User

views = Blueprint("views",__name__)

@views.route("/")
def home():
    if g.user:
        return render_template("profile/profile.html", user = g.user)
    return render_template("home/home.html")

@views.route("/<username>")
def profile_public(username):
    username = username.lower()
    user =  User.query.filter_by(username=username).first()
    if user:
        return render_template("profile/profile_public.html", user = user)
    else:
        return f"<p>No user named <strong>{username}</strong></p>"