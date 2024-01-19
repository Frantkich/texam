from flask import current_app
from flask_login import current_user
from requests import Session
from datetime import datetime
import bs4
import multiprocessing
import time

from app.tools.db.methods import (
    remove_exam_from_user, 
    add_exam_questions, 
    assign_exam_to_user, 
    bind_question_to_user, 
    get_question_in_exam,
    update_result_stats,
    update_result_questions,
    create_result,
    get_last_result,
    get_last_exam_results,
)


def new_tlc_session() -> Session:
    session = Session()
    data = {
        'ta_username': current_user.email,
        'ta_password': current_user.password,
        'login': "Login"
    }
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0'}
    response = session.post(current_app.config["TLCEXAM_URL"] + "/login", data=data, headers=headers)
    if response.status_code != 200: return None
    print(f"New session opened with user: {current_user.email.split('@')[0]} | Session ID: {session.cookies.get_dict().get('JSESSIONID')}")
    return session


def fetch_user_exams():
    session = new_tlc_session()
    if not session: return None
    response = session.get(current_app.config["TLCEXAM_URL"] + "/test_list")
    soup = bs4.BeautifulSoup(response.content, "html.parser")
    exams = []
    for row in soup.find_all("tr")[1:]:
        col = row.find_all("td")
        formated_name = col[1].text.replace(" ", "")
        formated_name = formated_name[:formated_name.index("-R")]
        exams.append({
            "code": col[0].find("input")['value'],
            "name": formated_name,
            "long_name": col[1].text,
            "description": col[2].text,
            "class_name": col[3].text
        })
    return exams


def load_questions(name: str):
    session, resp = open_exam(name)
    if not resp: return False
    html:str = resp.content
    soup = bs4.BeautifulSoup(html, "html.parser")
    index_start_nb_questions = html.find(b"Question 1 of ")
    index_end_nb_questions = html.find(b"\n", index_start_nb_questions + 1)
    nb_questions = int(html[index_start_nb_questions + 13:index_end_nb_questions])
    assign_exam_to_user(name)
    create_result()
    for _ in range(nb_questions):
        question_text = soup.find(id="questiontext").text
        question = get_question_in_exam(current_user.exam_id, question_text)
        if question:
            bind_question_to_user(question)
        else:
            exam = add_exam_questions(name, [{
                "description": question_text,
                "answers": [{"description": tr.find_all("td")[-1].text} for tr in soup.find_all("tr")[1:]]
            }])
            bind_question_to_user(exam.questions[-1])
        response = session.post(current_app.config["TLCEXAM_URL"] + "/display_question", data={"cmd": "", "next_ques": "Next>"})
        soup = bs4.BeautifulSoup(response.content, "html.parser")
    return True


def answering_questions() -> str:
    session, resp = open_exam(current_user.exam.code)
    html:str = resp.content
    soup = bs4.BeautifulSoup(html, "html.parser")
    index_start_nb_questions = html.find(b"Question 1 of ")
    index_end_nb_questions = html.find(b"\n", index_start_nb_questions + 1)
    nb_questions = int(html[index_start_nb_questions + 13:index_end_nb_questions])
    questions_processed = []
    for _ in range(nb_questions):
        question_text = soup.find(id="questiontext").text
        question = get_question_in_exam(current_user.exam_id, question_text)
        if not question: return 500 # LA QUESTION NE S'EST PAS BIEN ENREGISTREE
        question_processed = {
            "question" : {
                "id": question.id,
                "description": question.description,
            }
        }
        go_to_next_question = False
        taker_ans = None
        data = {"cmd": "", "next_ques": "Next>"}
        for index, tr in enumerate(soup.find_all("tr")[1:]): # ON PARCOURT LES REPONSES
            answer_desc = tr.find_all("td")[-1].text
            for answer in question.answers:
                if answer.description == answer_desc:
                    if answer.score == 2 or answer.score == 3:
                        question_processed["answer"] = {
                            "id": answer.id,
                            "description": answer.description,
                            "score": answer.score,
                            "remarks": answer.remarks
                        }
                        taker_ans = index + 1
                        tr.find("input")['checked'] = True
                        if answer.score == 3: go_to_next_question = True
            if taker_ans != None:
                data["taker_ans"] = taker_ans
            if go_to_next_question: break
        questions_processed.append(question_processed)
        # ON ENVOIE LA REPONSE
        response = session.post(current_app.config["TLCEXAM_URL"] + "/display_question", data=data)
        soup = bs4.BeautifulSoup(response.content, "html.parser")
    update_result_questions(get_last_exam_results(), questions_processed)
    return generate_report(session)


def generate_report(session:Session = None, fresh_start: bool = False) -> str:
    response = session.get(current_app.config["TLCEXAM_URL"] + "/summary_list")
    soup = bs4.BeautifulSoup(response.content, "html.parser")
    unanswered = sum([1 for row in soup.find_all('tr')[1:] if row.find_all('td')[3].text != "Answered"])
    question_count = len(soup.find_all('tr')[1:])
    answered_ratio = abs(((unanswered * 100) / question_count) - 100)
    return f"{answered_ratio}% of exam's responses answered."


def submit_exam_delay(delay:str) -> str:
    session = new_tlc_session()
    if not session: return None
    session.post(current_app.config["TLCEXAM_URL"] + "/test_list", data={"take_test": current_user.exam.code})
    session.get(current_app.config["TLCEXAM_URL"] + "/load_questions")
    resp = session.get(current_app.config["TLCEXAM_URL"] + "/show_timed")
    soup = bs4.BeautifulSoup(resp.content, "html.parser")
    time = soup.find(id="disclaimer").text
    time = time[time.find("have ") + 5: time.find(" minutes")]
    time = int(time) - ( int(delay) + 1 )
    if time <= 0: return None
    process = multiprocessing.Process(target=submit_exam(), args=(time * 60 ,))
    process.start()
    return time


def submit_sleep(delay:int):
    print(datetime.now())
    print(f"{delay} seconds")
    time.sleep(delay)
    print(datetime.now())
    return submit_exam()


def submit_exam():
    print("done")
    print(datetime.now())
    session, resp = open_exam(current_user.exam.code)
    resp = session.post(current_app.config["TLCEXAM_URL"] + "/summary_list", data={
        "done": "Finished+taking+Test",
        "curr_screen": "1",
        "skip_buttons": ""
    })
    soup = bs4.BeautifulSoup(resp.content, "html.parser")
    infos = soup.find_all(class_="metainforight")
    score = infos[0].text[13:].split(" ")[0],
    success = 0 if infos[1].text == "Failed" else 1
    detail_score = []
    for row in soup.find_all('tr')[1:]:
        columns = row.find_all('td')
        detail_score.append({
            "subject": columns[0].text,
            "noQuestions": columns[1].text,
            "score": columns[2].text
        })
    session.get(current_app.config["TLCEXAM_URL"] + "/summary_list?exit_page=1")
    result = update_result_stats(get_last_result(), success, score, detail_score, ended=True)
    remove_exam_from_user()
    return result


def open_exam(code:str) -> Session:
    session = new_tlc_session()
    if not session: return None
    resp = session.post(current_app.config["TLCEXAM_URL"] + "/test_list", data={"take_test": code})
    if resp.status_code != 200 or resp.text.find("You cannot take this test") != -1: return None, None
    session.get(current_app.config["TLCEXAM_URL"] + "/load_questions")
    session.get(current_app.config["TLCEXAM_URL"] + "/show_timed")
    session.get(current_app.config["TLCEXAM_URL"] + "/begin_test_message")
    resp = session.post(current_app.config["TLCEXAM_URL"] + "/summary_list", data={
        "go": "Go+back+to+selected+question",
        "go_q": "1",
        "curr_screen": "1",
        "skip_buttons": ""
    })
    if resp.status_code != 200: return None, None
    return session, resp
