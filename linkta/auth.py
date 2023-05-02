import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from . import db
from .models import User

auth = Blueprint("auth",__name__)

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exists =  User.query.filter_by(email=email).first()
        username_exists =  User.query.filter_by(username=username).first()

        if email_exists:
            flash("Email already in use", category="error")
        elif username_exists:
            flash("Username already taken", category="error")
        elif password1 != password2:
            flash("Passwords do not match", category="error")
        elif len(password1) <= 6:
            flash("Password must be more than six characters", category="error")
        else:
            user = User(email = email, username = username, fname = fname, lname = lname, password = generate_password_hash(password1))
            db.session.add(user)
            db.session.commit()
            flash("Account created successfully", category="success")

    return render_template("forms/signup.html")