import os


class Config:
    # general
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'change-me-change-me'

    # database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # jwt
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-string'
