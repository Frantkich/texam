from flask import current_app
from flask_login import current_user
import requests
import bs4

from app.tools.db import get_exam


def new_tlc_session():
    session = requests.Session()
    data = {
        'ta_username': current_user.email,
        'ta_password': current_user.password,
        'login': "Login"
    }
    headers = {'User-Agent': 'Your User Agent'}
    response = session.post(current_app.config["TLCEXAM_URL"] + "/login", data=data, headers=headers)
    
    if response.status_code != 200:
        return None
    session_id = session.cookies.get_dict().get('JSESSIONID')
    print(f"Session ID: {session_id}")
    return session

def fetch_new_exams():
    # session = new_tlc_session()
    # if not session: return None
    
    # response = session.get(current_app.config["TLCEXAM_URL"] + "/test_list")
    # soup = bs4.BeautifulSoup(response.content, "html.parser")
    
    with open("C:\\Users\\Frantkich\\Desktop\\texam\\html.html", "r") as file:
        html_content = file.read()
    
    soup = bs4.BeautifulSoup(html_content, "html.parser")

    exams = []
    for tr in soup.find_all("tr")[1:]:
        tds = tr.find_all("td")
        exams.append({
            "code": tds[0].find("input")['value'],
            "name": tds[1].text,
            "description": tds[2].text,
            "class_name": tds[3].text
        })
    return exams


def fetch_new_questions(exam_code: str):
    # session = new_tlc_session()
    # if not session: return None

    questions = []
    while True:
        # response = session.post(current_app.config["TLCEXAM_URL"] + "/test_list", data={"take_test": exam.code})
        questions.append({
            "description": "FOPM enables a bank to express relationships with a client via",
            "answers": [
                {
                    "description": "third party"
                },
                {
                    "description": "third party with client_f=1"
                },
                {
                    "description": "Both"
                },
                {
                    "description": "None"
                }
            ]
        })
        if True:
            break
    return questions

def pass_exam(exam_code: str):
    session = new_tlc_session()
    if not session: return None

    # response = session.post(current_app.config["TLCEXAM_URL"] + "/test_list", data={"take_test": exam_code})

    return True
