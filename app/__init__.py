import os
import csv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# global extensions
db = SQLAlchemy()
jwt = JWTManager()


def ensure_csv(path, header):
    """Create a CSV file with header if it does not exist or is empty."""
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    if not os.path.exists(path) or os.path.getsize(path) == 0:
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        # import parts of our application
        from . import routes, models

        # register blueprints
        app.register_blueprint(routes.bp)

        # create database tables
        db.create_all()

        # ensure data files exist with headers
        ensure_csv('data/mood_dataset.csv', ['text', 'sentiment'])
        ensure_csv('data/training_data.csv', ['text', 'sentiment'])

        # make sure sentiment model is trained at start
        try:
            from .ml_model import train
            train()
        except Exception:
            pass

    return app
