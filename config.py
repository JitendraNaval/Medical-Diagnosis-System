import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '5791628bb0b13ce0c676dfde280ba245'
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'medical_diagnosis.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
