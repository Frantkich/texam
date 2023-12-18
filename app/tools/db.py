from flask import current_app, g

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class Base(DeclarativeBase):
  pass

db_connector = SQLAlchemy(model_class=Base)


class User(db_connector.Model):
    id: Mapped[int]       = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)

with current_app.app_context():
    db_connector.create_all()

def get_user(email):
   return db_connector.get_or_404(User, email)
