from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    Text,
    DateTime,
    PickleType,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from typing import List
from datetime import datetime


class Base(DeclarativeBase):
    pass


db_c = SQLAlchemy(model_class=Base)


user_question = Table(
    "user_question",
    db_c.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("question_id", ForeignKey("questions.id"), primary_key=True),
)


class Users(UserMixin, db_c.Model):
    id: Mapped[int]                     = mapped_column(Integer, primary_key=True)
    email: Mapped[str]                  = mapped_column(String(255), unique=True)
    password: Mapped[str]               = mapped_column(String(255), nullable=False)
    is_admin: Mapped[bool]              = mapped_column(Boolean, default=False)
    exam_id: Mapped[int]                = mapped_column(ForeignKey("exams.id"), nullable=True)
    exam: Mapped["Exams"]               = relationship()


class Exams(db_c.Model):
    id: Mapped[int]                     = mapped_column(Integer, primary_key=True)
    name: Mapped[str]                   = mapped_column(String(255), unique=True)
    long_name: Mapped[str]              = mapped_column(String(255))
    code: Mapped[str]                   = mapped_column(String(255), unique=True)
    class_name: Mapped[str]             = mapped_column(String(255))
    description: Mapped[str]            = mapped_column(String(2042))
    questions: Mapped[List["Questions"]]= relationship(cascade="all, delete-orphan")


class Questions(db_c.Model):
    id: Mapped[int]                     = mapped_column(Integer, primary_key=True)
    description: Mapped[str]            = mapped_column(String(2042))
    exam_id: Mapped[int]                = mapped_column(ForeignKey("exams.id"))
    user_id: Mapped[int]                = mapped_column(ForeignKey("users.id"))
    answers: Mapped[List["Answers"]]    = relationship(cascade="all, delete-orphan")
    active_for: Mapped[List["Users"]]   = relationship(secondary=user_question)
    user_last_answer: Mapped["Users"]   = relationship()


class Answers(db_c.Model):
    id: Mapped[int]                     = mapped_column(Integer, primary_key=True)
    description: Mapped[str]            = mapped_column(String(2042))
    score: Mapped[int]                  = mapped_column(Integer, nullable=True)
    remarks: Mapped[str]                = mapped_column(Text(2042), nullable=True)
    question_id: Mapped[int]            = mapped_column(ForeignKey("questions.id"))


class Results(db_c.Model):
    id: Mapped[int]                     = mapped_column(Integer, primary_key=True)
    date: Mapped[datetime]              = mapped_column(DateTime)
    success: Mapped[bool]               = mapped_column(Boolean, nullable=True)
    score: Mapped[str]                  = mapped_column(String(255), nullable=True)
    detail_score: Mapped[dict]          = mapped_column(PickleType, nullable=True)
    submitted_questions: Mapped[dict]   = mapped_column(PickleType, nullable=True)
    ended: Mapped[bool]                 = mapped_column(Boolean, default=False)
    user_id: Mapped[int]                = mapped_column(ForeignKey("users.id"))
    exam_id: Mapped[int]                = mapped_column(ForeignKey("exams.id"))
    exam: Mapped["Exams"]               = relationship()
    user: Mapped["Users"]               = relationship()
