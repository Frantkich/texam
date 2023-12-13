import os


class Config(object):
    SECRET_KEY = "soumia_bagnicong_de_la_keifuern"
    TEMPLATE_FOLDER = os.getcwd() + "/app/templates"
    STATIC_FOLDER = os.getcwd() + "/app/static"
    MONGO_USERNAME = "username"
    MONGO_PASSWORD = "password"
    MONGO_HOST = "frantkich.fr"
    MONGO_COLLECTION = "collectionX"
    MONGO_URI = (f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}/{MONGO_COLLECTION}")


configs = {"dev": Config}
