from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

views = Blueprint("views",__name__)

@views.route("/")
def home():
    if g.user:
        return render_template("profile/profile.html", user = g.user)
    return render_template("home/home.html")