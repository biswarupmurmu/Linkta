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
        email = request.form.get("email").lower()
        username = request.form.get("username").lower()
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exists =  User.query.filter_by(email=email).first()
        username_exists =  User.query.filter_by(username=username).first()

        if email_exists:
            flash("Email already in use", category="error")
            return redirect(request.url)
        elif username_exists:
            flash("Username already taken", category="error")
            return redirect(request.url)
        elif password1 != password2:
            flash("Passwords do not match", category="error")
            return redirect(request.url)
        elif len(password1) <= 6:
            flash("Password must be more than six characters", category="error")
            return redirect(request.url)
        else:
            user = User(email = email, username = username, fname = fname, lname = lname, password = generate_password_hash(password1))
            db.session.add(user)
            db.session.commit()
            flash("Account created successfully", category="success")
            return redirect(url_for("auth.login"))

    return render_template("forms/signup.html")

# login
@auth.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":

        emailorusername = request.form.get("emailorusername").lower()
        password = request.form.get("password")

        user =  User.query.filter_by(username = emailorusername).first()
        if not user:
            user =  User.query.filter_by(email = emailorusername).first()

        if user:
            if not check_password_hash(user.password, password):
                flash("Incorrect password",category="error")
                return redirect(request.url)
            else:
                session.clear()
                session['user_id'] = user.id
                flash(f"You are logged in as {user.username} successfully", category="success")
                return redirect(url_for("views.home"))
        else:
            flash("Invalid username or email", category="error")
            return redirect(request.url)

    return render_template("forms/login.html")

# stay logged in
@auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()

# log in required
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view

# logout
@auth.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("views.home"))