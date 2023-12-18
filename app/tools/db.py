from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, PickleType
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import json

import pymysql
pymysql.install_as_MySQLdb()

class Base(DeclarativeBase):
  pass
db_c = SQLAlchemy(model_class=Base)

class Users(UserMixin, db_c.Model):
    id: Mapped[int]       = mapped_column(Integer, primary_key=True)
    email: Mapped[str]    = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)


class Exams(UserMixin, db_c.Model):
    id: Mapped[int]         = mapped_column(Integer, primary_key=True)
    name: Mapped[str]       = mapped_column(String(255), unique=True, nullable=False)
    questions: Mapped[dict] = mapped_column(PickleType, nullable=False)


def get_user(email:str) -> Users:
   return Users.query.filter_by(email=email).first()

def get_exam(name:str) -> Exams:
   return Exams.query.filter_by(name=name).first()

def get_all_exam() -> Exams:
   return Exams.query.all()

def create_exam(name:str, questions:dict) -> Exams:
   exam:Exams = Exams(name=name, questions=json.dumps(questions))
   db_c.session.add(exam)
   db_c.session.commit()
   return exam

def add_exam_questions(name:str, questions:dict) -> Exams:
   exam:Exams = Exams.query.filter_by(name=name).first()
   if not exam:
      return None
   exam.questions += json.dumps(questions)
   db_c.session.commit()
   return exam
