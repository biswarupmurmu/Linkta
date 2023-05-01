from flask import Flask

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    )
    app.config.from_pyfile('config.py', silent=True)

    from .views import views
    app.register_blueprint(views, url_prefix="/")

    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app