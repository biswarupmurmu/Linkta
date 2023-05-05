from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from .models import User
from .auth import login_required
from . import db
from werkzeug.utils import secure_filename
import os
import uuid as uuid
from . import UPLOAD_FOLDER
from . import FILE_EXTENSIONS

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

        if 'profile_picture' in request.files:
            profile_picture = request.files['profile_picture']
            if profile_picture and not allowed_file(profile_picture.filename, FILE_EXTENSIONS['image']):
                flash('Can not update profile picture.', category="error")
            if profile_picture.filename != '' and allowed_file(profile_picture.filename, FILE_EXTENSIONS['image']) and profile_picture:
                filename = secure_filename(profile_picture.filename)
                profile_picture_name = str(uuid.uuid1()) + "_" + filename
                profile_picture.save(os.path.join(UPLOAD_FOLDER, profile_picture_name))
                previous_profile_picture = g.user.profile_picture
                g.user.profile_picture = profile_picture_name
        
        if 'cover_picture' in request.files:
            cover_picture = request.files['cover_picture']
            if cover_picture and not allowed_file(cover_picture.filename, FILE_EXTENSIONS['image']):
                flash('Can not update cover picture.', category="error")
            if cover_picture.filename != '' and allowed_file(cover_picture.filename, FILE_EXTENSIONS['image']) and cover_picture:
                filename = secure_filename(cover_picture.filename)
                cover_picture_name = str(uuid.uuid1()) + "_" + filename
                cover_picture.save(os.path.join(UPLOAD_FOLDER, cover_picture_name))
                previous_cover_picture = g.user.cover_picture
                g.user.cover_picture = cover_picture_name

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
            g.user.username = new_username
        g.user.contact_email = new_contact_email
        g.user.fname = new_fname
        g.user.lname = new_lname
        g.user.about = new_about
        g.user.public_view = public_view
        g.user.whoami = new_whoami
        db.session.commit()

        # Delete previous profile picture
        try:
            os.remove(UPLOAD_FOLDER + "/" + previous_profile_picture)
        except:
            pass
        # Delete previous cover picture
        try:
            os.remove(UPLOAD_FOLDER + "/" + previous_cover_picture)
        except:
            pass

        flash("Account updated successfully", category="success")
        return redirect(request.url)

    return render_template("profile/profile_edit.html", user = g.user)

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions