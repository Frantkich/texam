from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.types import JSON

import pymysql
pymysql.install_as_MySQLdb()

class Base(DeclarativeBase):
  pass
db_c = SQLAlchemy(model_class=Base)


class Users(UserMixin, db_c.Model):
    id: Mapped[int]       = mapped_column(Integer, primary_key=True)
    email: Mapped[str]    = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_admin: Mapped[bool]= mapped_column(db_c.Boolean, default=False)


class Exams(UserMixin, db_c.Model):
    id: Mapped[int]         = mapped_column(Integer, primary_key=True)
    name: Mapped[str]       = mapped_column(String(255), unique=True, nullable=False)
    code: Mapped[str]       = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str]= mapped_column(String(255), nullable=False)
    class_name: Mapped[str] = mapped_column(String(255), nullable=False)
    questions: Mapped[dict] = mapped_column(MutableDict.as_mutable(JSON), nullable=False)

    # FORMAT QUESTIONS
    # questions = [
    #     {
    #         "description": "description",
    #         "answers": [{
    #             "description": "description",
    #             "score": 7
    #         },...
    #         }],
    #     },...
    # ]


def get_user(email:str) -> Users:
   return Users.query.filter_by(email=email).first()

def get_exam(code:str) -> Exams:
   return Exams.query.filter_by(code=code).first()

def get_all_exam() -> Exams:
   return Exams.query.all()

def create_exam(name:str, code:str, description:str, class_name:str, questions:dict) -> Exams:
   exam:Exams = Exams(name=name, code=code, description=description, class_name=class_name, questions=questions)
   db_c.session.add(exam)
   db_c.session.commit()
   return exam

def update_exam_questions(code:str, questions:dict) -> Exams:
   exam:Exams = Exams.query.filter_by(code=code).first()
   if not exam:
      return None
   exam.questions = questions
   db_c.session.commit()
   return exam

def add_exam_question(code:str, new_questions:dict) -> Exams:
   exam:Exams = Exams.query.filter_by(code=code).first()
   for new_question in new_questions:
      if not [1 for question in exam.questions["questions"] if question["description"] == new_question["description"]]:
         exam.questions["questions"].append(new_question)
   print("NEW QUESTIONS")
   print(exam.questions)
   db_c.session.commit()
   return exam