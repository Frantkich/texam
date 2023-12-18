import os


class Config(object):
    SECRET_KEY = "soumia_bagnicong_de_la_keifuern"
    TEMPLATE_FOLDER = os.getcwd() + "/app/templates"
    STATIC_FOLDER = os.getcwd() + "/app/static"
    SQL_USERNAME = "syncordian"
    SQL_HOST = "localhost"
    SQL_DATABASE = "texam"
    SQLALCHEMY_DATABASE_URI = (f"mysql://{SQL_USERNAME}@{SQL_HOST}:3306/{SQL_DATABASE}")


configs = {"dev": Config}
