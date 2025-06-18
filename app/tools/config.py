import os


class Config(object):
    PROJECT_NAME = "texam"
    SQL_DATABASE = PROJECT_NAME
    SECRET =
    SECRET_KEY =
    TLCEXAM_URL =
    TEMPLATE_FOLDER = os.getcwd() + "/app/templates"
    STATIC_FOLDER = os.getcwd() + "/app/static"
    SQL_USERNAME = 
    SQL_HOST = 
    SQLALCHEMY_DATABASE_URI = (f"mysql://{SQL_USERNAME}@{SQL_HOST}:3306/{SQL_DATABASE}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_recycle": 360}


configs = {"config": Config}
