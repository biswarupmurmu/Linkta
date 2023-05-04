from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from .models import User
from .auth import login_required
from . import db

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
        if user.public_view:
            return render_template("profile/profile_public.html", user = user)
        else:
            return f"<p>No user named <strong>{username}</strong></p>"
    else:
        return f"<p>No user named <strong>{username}</strong></p>"
    
@views.route("/edit", methods = ['GET','POST'])
@login_required
def profile_edit():
    if request.method == 'POST':
        new_contact_email = request.form.get("contact_email")
        new_username = request.form.get("username").lower()
        new_fname = request.form.get("fname")
        new_lname = request.form.get("lname")
        new_about = request.form.get("about")
        new_whoami = request.form.get("whoami")
        public_view = request.form.get("public_view")
        if public_view:
            public_view = True
        else:
            public_view = False

        username_exists = None
        if new_username != g.user.username:
            username_exists = User.query.filter_by(username=new_username).first()
            if username_exists:
                flash("Username already exists", category="error")

        if not username_exists:
            g.user.contact_email = new_contact_email
            g.user.username = new_username
            g.user.fname = new_fname
            g.user.lname = new_lname
            g.user.about = new_about
            g.user.public_view = public_view
            g.user.whoami = new_whoami
            db.session.commit()
            flash("Account updated successfully", category="success")
            return redirect(request.url)

    return render_template("profile/profile_edit.html", user = g.user)