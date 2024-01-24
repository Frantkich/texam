import os


class Config(object):
    PROJECT_NAME = "texam"
    SQL_DATABASE = PROJECT_NAME
    SECRET = "tlcsucks"
    SECRET_KEY = "El_Christ_bagnicong_de_la_keifuern"
    TLCEXAM_URL = "https://tlcexams.temenos.com/partner"
    TEMPLATE_FOLDER = os.getcwd() + "/app/templates"
    STATIC_FOLDER = os.getcwd() + "/app/static"
    SQL_USERNAME = "syncordian"
    SQL_HOST = "frantkich.fr"
    SQLALCHEMY_DATABASE_URI = (f"mysql://{SQL_USERNAME}@{SQL_HOST}:3306/{SQL_DATABASE}")


configs = {"config": Config}
