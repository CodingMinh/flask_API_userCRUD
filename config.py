""" configuration variables """
# activate venv: & "C:\Users\Hi Windows 11 23\Desktop\Python\flask_API_userCRUD\.venv\Scripts\Activate.ps1"
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')