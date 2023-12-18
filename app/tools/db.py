from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

import pymysql
pymysql.install_as_MySQLdb()


class Base(DeclarativeBase):
  pass
db_connector = SQLAlchemy(model_class=Base)

class Users(UserMixin, db_connector.Model):
    id: Mapped[int]       = mapped_column(Integer, primary_key=True)
    email: Mapped[str]    = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)


def get_user(email:str) -> Users:
   return Users.query.filter_by(email=email).first()
