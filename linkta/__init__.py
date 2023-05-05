from flask import Flask
import os

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

UPLOAD_FOLDER = os.path.join('linkta/static', 'user_uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI = "sqlite:///database.db",
        MAX_CONTENT_LENGTH = 16 * 1000 * 1000,
        UPLOAD_FOLDER = UPLOAD_FOLDER
    )
    app.config.from_pyfile('config.py', silent=True)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    # ensure the UPLOAD folder exists
    try:
        os.makedirs(UPLOAD_FOLDER)
    except OSError:
        pass

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app