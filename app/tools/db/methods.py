from flask_login import current_user
from sqlalchemy import and_
from datetime import datetime
import json


from app.tools.db.models import * 


# Users
def get_user(email:str) -> Users:
    return Users.query.filter_by(email=email).first()


def assign_exam_to_user(exam_name:str):
    exam:Exams = get_exams(exam_name)
    if not exam: return False
    current_user.exam = exam
    db_c.session.commit()
    return True


def remove_exam_from_user():
    for question in Questions.query.filter(and_(Questions.exam_id == current_user.exam_id, Questions.active_for.any(id=current_user.id))).all():
        question.active_for.remove(current_user)
    current_user.exam = None
    db_c.session.commit()
    return True


def bind_question_to_user(question:Questions) -> Questions:
    question.active_for.append(current_user)
    db_c.session.commit()
    return question


# Exams
def get_exams(name:str=None) -> Exams:
    if not name:
        return Exams.query.all()
    else:
        return Exams.query.filter_by(name=name).first()


def create_exam(name:str, code:str, long_name:str, description:str, class_name:str) -> Exams:
    exam:Exams = Exams(name=name, long_name=long_name, code=code, description=description, class_name=class_name)
    db_c.session.add(exam)
    db_c.session.commit()
    return exam

def update_exam(exams) -> Exams:
    for exam in exams:
        existing_exam = get_exams(exam["name"])
        if not existing_exam:
            create_exam(exam["name"], exam["long_name"], exam["code"], exam["description"], exam["class_name"])
        elif existing_exam.code != exam["code"]:
            existing_exam.long_name = exam["long_name"]
            existing_exam.code = exam["code"]
    db_c.session.commit()
    return exam

# Questions
def get_question_in_exam(exam_id, question_desc:str) -> Questions:
    return Questions.query.filter(and_(Questions.exam_id == exam_id, Questions.description == question_desc)).first()


def search_questions(id:int = None, search_string:str = None) -> Questions:
    if id:
        return Questions.query.filter_by(id=id).first()
    elif search_string:
        return Questions.query.filter(Questions.description.like(f"%{search_string}%")).all()
    else:
        return None


def get_all_questions() -> Questions:
    return Questions.query.all()


def update_exam_questions(name:str, questions:dict) -> Exams:
    exam:Exams = Exams.query.filter_by(name=name).first()
    if not exam:
        return None
    for question in questions:
        answer_db = None
        for answer in question["answers"]:
            answer_db:Answers = Answers.query.filter_by(id=answer["id"]).first()
            if answer_db:
                answer_db.remarks = answer["remarks"]
                if "score" in answer:
                    if not answer["score"]:
                        answer_db.score = None
                    elif answer["score"].isnumeric():
                        answer_db.score = int(answer["score"])
                    else:
                        answer_db.score = None
            else:
                return None
        question_db:Questions = Questions.query.filter_by(id=answer_db.question_id).first()
        question_db.user_last_answer = current_user
    db_c.session.commit()
    return exam


def add_exam_questions(name:str, new_questions:list) -> Exams:
    exam:Exams = Exams.query.filter_by(name=name).first()
    for new_question in new_questions:
        if not [1 for old_question in exam.questions if old_question.description == new_question["description"]]:
            answers = []
            for answer in new_question["answers"]:
                score = answer["score"] if "score" in answer else None
                remarks = answer["remarks"] if "remarks" in answer else None
                answers.append(Answers(description=answer["description"], score=score, remarks=remarks))
            exam.questions.append(Questions(description=new_question["description"], answers=answers, user_last_answer=current_user))
    db_c.session.commit()
    return exam


# Results
def create_result() -> Results:
    result:Results = Results(date=datetime.now(), user=current_user, exam=current_user.exam)
    db_c.session.add(result)
    db_c.session.commit()
    return result


def update_result_stats(result:Results, success:bool, score:str, detail_score:dict, ended:bool=False) -> Results:
    result.detail_score = json.dumps(detail_score)
    result.success = success
    result.score = score
    result.ended = ended
    db_c.session.commit()
    return result


def update_result_questions(result:Results, submitted_questions:dict) -> Results:
    result.submitted_questions = json.dumps(submitted_questions)
    db_c.session.commit()
    return result


def get_last_result() -> Results:
    return Results.query.filter_by(user_id=current_user.id).order_by(Results.date.desc()).first()


def get_user_results(id:int = None) -> Results:
    if not id:
        return Results.query.filter_by(user_id=current_user.id).all()
    else:
        return Results.query.filter_by(id=id).first_or_404()

def get_last_exam_results() -> Results:
    return Results.query.filter(
        and_(
            Results.user_id == current_user.id, 
            Results.exam_id == current_user.exam_id
        )).order_by(Results.date.desc()).first()

def get_exam_results(exam_id:int = None) -> Results:
    return Results.query.filter_by(exam_id=exam_id).all()
