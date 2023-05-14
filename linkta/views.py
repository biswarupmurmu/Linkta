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
        
        # Links
        new_linkedin = request.form.get("linkedin").lower()
        new_github = request.form.get("github").lower()
        new_medium = request.form.get("medium").lower()
        new_website = request.form.get("website").lower()
        new_portfolio = request.form.get("portfolio").lower()
        new_leetcode = request.form.get("leetcode").lower()
        new_codechef = request.form.get("codechef").lower()
        new_hackerrank = request.form.get("hackerrank").lower()
        new_facebook = request.form.get("facebook").lower()
        new_instagram = request.form.get("instagram").lower()
        new_twitter = request.form.get("twitter").lower()

        # Visibility settings
        public_view = request.form.get("public_view")
        if public_view:
            public_view = True
        else:
            public_view = False

        linkedin_view = request.form.get("linkedin_view")
        if linkedin_view:
            linkedin_view = True
        else:
            linkedin_view = False
        
        github_view = request.form.get("github_view")
        if github_view:
            github_view = True
        else:
            github_view = False

        medium_view = request.form.get("medium_view")
        if medium_view:
            medium_view = True
        else:
            medium_view = False   

        website_view = request.form.get("website_view")
        if website_view:
            website_view = True
        else:
            website_view = False            

        portfolio_view = request.form.get("portfolio_view")
        if portfolio_view:
            portfolio_view = True
        else:
            portfolio_view = False

        leetcode_view = request.form.get("leetcode_view")
        if leetcode_view:
            leetcode_view = True
        else:
            leetcode_view = False

        codechef_view = request.form.get("codechef_view")
        if codechef_view:
            codechef_view = True
        else:
            codechef_view = False     

        hackerrank_view = request.form.get("hackerrank_view")
        if hackerrank_view:
            hackerrank_view = True
        else:
            hackerrank_view = False

        facebook_view = request.form.get("facebook_view")
        if facebook_view:
            facebook_view = True
        else:
            facebook_view = False

        instagram_view = request.form.get("instagram_view")
        if instagram_view:
            instagram_view = True
        else:
            instagram_view = False

        twitter_view = request.form.get("twitter_view")
        if twitter_view:
            twitter_view = True
        else:
            twitter_view = False

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
        g.user.whoami = new_whoami
        # Links
        g.user.linkedin = new_linkedin
        g.user.github = new_github
        g.user.medium = new_medium
        g.user.website = new_website
        g.user.portfolio = new_portfolio
        g.user.leetcode = new_leetcode
        g.user.codechef = new_codechef
        g.user.hackerrank = new_hackerrank
        g.user.facebook = new_facebook
        g.user.instagram = new_instagram
        g.user.twitter = new_twitter
        # visibility settings
        g.user.public_view = public_view
        g.user.linkedin_view = linkedin_view
        g.user.github_view = github_view
        g.user.medium_view = medium_view
        g.user.website_view = website_view
        g.user.portfolio_view = portfolio_view
        g.user.leetcode_view = leetcode_view
        g.user.codechef_view = codechef_view
        g.user.hackerrank_view = hackerrank_view
        g.user.facebook_view = facebook_view
        g.user.instagram_view = instagram_view
        g.user.twitter_view = twitter_view
        # Update
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