from flask_login import UserMixin, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List
import pymysql
pymysql.install_as_MySQLdb()

class Base(DeclarativeBase):
  pass
db_c = SQLAlchemy(model_class=Base)

# Models

class Users(UserMixin, db_c.Model):
    id: Mapped[int]                      = mapped_column(Integer,     primary_key=True)
    email: Mapped[str]                   = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str]                = mapped_column(String(255), nullable=False)
    is_admin: Mapped[bool]               = mapped_column(Boolean,     default=False)
    exam_id: Mapped[int]                 = mapped_column(ForeignKey("exams.id"), nullable=True)
    exam: Mapped["Exams"]                = relationship()


class Exams(db_c.Model):
    id: Mapped[int]                      = mapped_column(Integer,     primary_key=True)
    name: Mapped[str]                    = mapped_column(String(255), nullable=False, unique=True)
    code: Mapped[str]                    = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str]             = mapped_column(String(255), nullable=False)
    class_name: Mapped[str]              = mapped_column(String(255), nullable=False)
    questions: Mapped[List["Questions"]] = relationship(cascade="all, delete-orphan")

class Questions(db_c.Model):
    id: Mapped[int]                      = mapped_column(Integer,     primary_key=True)
    description: Mapped[str]             = mapped_column(String(255), nullable=False)
    exam_id: Mapped[int]                 = mapped_column(ForeignKey("exams.id"))
    answers: Mapped[List["Answers"]]     = relationship(cascade="all, delete-orphan")


class Answers(db_c.Model):
    id: Mapped[int]                      = mapped_column(Integer,     primary_key=True)
    description: Mapped[str]             = mapped_column(String(255), nullable=False)
    score: Mapped[int]                   = mapped_column(Integer,     nullable=True)
    remarks: Mapped[str]                 = mapped_column(Text(2042), nullable=True)
    question_id: Mapped[int]             = mapped_column(ForeignKey("questions.id"))


def get_user(email:str) -> Users:
    return Users.query.filter_by(email=email).first()


def assign_exam_to_user(exam_code:str):
    exam:Exams = get_exam(exam_code)
    if not exam: return False
    current_user.exam = exam
    db_c.session.commit()
    return True


def remove_exam_from_user():
    current_user.exam = None
    db_c.session.commit()
    return True


def get_exam(code:str) -> Exams:
    return Exams.query.filter_by(code=code).first()


def get_all_exams() -> Exams:
    return Exams.query.all()


def get_question(id:int = None, search_string:str = None) -> Questions:
    if id:
        return Questions.query.filter_by(id=id).first()
    elif search_string:
        return Questions.query.filter(Questions.description.like(f"%{search_string}%")).all()
    else:
        return None


def get_all_questions() -> Questions:
    return Questions.query.all()


def create_exam(name:str, code:str, description:str, class_name:str) -> Exams:
    exam:Exams = Exams(name=name, code=code, description=description, class_name=class_name)
    db_c.session.add(exam)
    db_c.session.commit()
    return exam


def update_exam_questions(code:str, questions:dict) -> Exams:
    exam:Exams = Exams.query.filter_by(code=code).first()
    if not exam:
        return None
    for question in questions:
        for answer in question["answers"]:
            answer_db:Answers = Answers.query.filter_by(id=answer["id"]).first()
            if answer_db:
                answer_db.remarks = answer["remarks"]
                if answer["score"].isnumeric():
                    answer_db.score = int(answer["score"])
                elif not answer["score"]:
                    answer_db.score = None
                else:
                    return None
            else:
                return None
    db_c.session.commit()
    return exam


def add_exam_question(code:str, new_questions:dict) -> Exams:
    exam:Exams = Exams.query.filter_by(code=code).first()
    for new_question in new_questions:
        if not [1 for old_question in exam.questions if old_question.description == new_question["description"]]:
            answers = []
            for answer in new_question["answers"]:
                answers.append(Answers(description=answer["description"]))
            exam.questions.append(Questions(description=new_question["description"], answers=answers))
    db_c.session.commit()
    return exam