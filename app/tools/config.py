import os


class Config(object):
    SECRET_KEY = "El_Christ_bagnicong_de_la_keifuern"
    TLCEXAM_URL = "https://tlcexams.temenos.com/partner"
    TEMPLATE_FOLDER = os.getcwd() + "/app/templates"
    STATIC_FOLDER = os.getcwd() + "/app/static"
    SQL_USERNAME = "syncordian"
    SQL_HOST = "192.168.1.190"
    SQL_DATABASE = "texam"
    SQLALCHEMY_DATABASE_URI = (f"mysql://{SQL_USERNAME}@{SQL_HOST}:3306/{SQL_DATABASE}")


configs = {"dev": Config}
