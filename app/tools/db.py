from flask import current_app, g
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
from flask_login import UserMixin


class User(UserMixin):
    pass


local_db = {"1@1.1": {"password": "1"}}


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = PyMongo(current_app).db
    return db


db = LocalProxy(get_db)


def insert_one(name):
    doc = {"name": name}
    return db.collectionX.insert_one(doc)


def find(query):
    return db.collectionX.find(query)


def update(_id, name):
    return db.collectionX.update_one({"_id": _id}, {"$set": {"name ": name}})


def delete(_id):
    return db.collectionX.delete_one({"_id": _id})


def get_user(email):
    return local_db[email] if email in local_db else None
    # return find({"email": email})
