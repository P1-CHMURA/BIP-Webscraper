from flask import Flask

from .extensions import db
from .views import main
from .utils import make_celery


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SECRET_KEY"] = "super-secret-key"
    app.config["CELERY_CONFIG"] = {"broker_url": "redis://localhost:6379/0","result_backend": "redis://redis_S:6379/0"}
    app.config["REDBEAT_SCHEDULE"] = {}
    app.config["REDBEAT_REDIS_URL"] = "redis://localhost:6379/0"  # Redis URL for scheduler
    app.config["REDBEAT_LOCK_KEY"] = "redbeat:lock"  # Lock key for Redbeat
    app.config["REDBEAT_MAX_INTERVAL"] = 30


    db.init_app(app)

    app.register_blueprint(main)

    celery = make_celery(app)
    celery.set_default()

    return app, celery