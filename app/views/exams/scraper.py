from flask import current_app
from flask_login import current_user
from requests import Session
import bs4

from app.tools.db import get_question, remove_exam_from_user, add_exam_question, assign_exam_to_user


def new_tlc_session() -> Session:
    return None
    session = Session()
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
    
    with open("C:\\Users\\Frantkich\\Desktop\\texam\\fetch_new_exams.html", "r") as file:
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

def load_questions(exam_code: str):
    soup, nb_questions = open_exam(exam_code)
    assign_exam_to_user(exam_code)
    for _ in range(nb_questions):
        # ATTENTION IL PEUT Y AVOIR UN \n DANS LA QUESTION
        question_text = soup.find(id="questiontext").text
        print(f"Question: '{question_text}'")
        question = get_question(search_string=question_text)
        if question:
            question.active_for.append(current_user)
        else:
            add_exam_question(exam_code, {
                "description": question_text,
                "answers": [{"description": tr.find("td").text} for tr in soup.find_all("tr")[1:]]
            })
        break
    return True

def submit_exam():
    soup, nb_questions = open_exam(current_user.exam.code)
    for _ in range(nb_questions):
        # ATTENTION IL PEUT Y AVOIR UN \n DANS LA QUESTION
        question_text = soup.find(id="questiontext").text
        print(f"Question: '{question_text}'")
        question = get_question(search_string=question_text)
        if not question: # LA QUESTION NE S'EST PAS BIEN ENREGISTREE
            return 500
        stop = False
        for index, tr in enumerate(soup.find_all("tr")[1:]):
            for answer in question.answers:
                if answer.description == tr.find("td").text:
                    if answer.score == 2 or answer.score == 3:
                        # response = session.post(current_app.config["TLCEXAM_URL"] + "/display_question", data={
                        #     "cmd": "",
                        #     "next_ques": "Next>",
                        #     "taker_ans": index
                        # })
                        # soup = bs4.BeautifulSoup(response.content, "html.parser")
                        tr.find("input")['checked'] = True
                        if answer.score is 3: stop = True
                    break
            if stop:
                break
        break
    # response = session.post(current_app.config["TLCEXAM_URL"] + "/summary_list", data={
    #     "done": "Finished+taking+Test",
    #     "curr_screen": "1",
    #     "skip_buttons": ""
    # })
    # soup = bs4.BeautifulSoup(response.content, "html.parser")
    with open("C:\\Users\\Frantkich\\Documents\\Syncordis\\texam\\summary_list_END.htm", "r") as file:
        html_content = file.read()
    soup = bs4.BeautifulSoup(html_content, "html.parser")
    total = soup.find(class_="your-class-name").text.split("</span> ")[1]
    result = soup.find_all("metainforight")[1].text
    print(f"Total: '{total}'")
    print(f"Result: '{result}'")

    detailed_result = []
    for row in soup.find_all('tr')[1:]:
        columns = row.find_all('td')
        detailed_result.append({
            "Subject": columns[0].text,
            "NoQuestions": columns[1].text,
            "Score": columns[2].text
        })

    print(detailed_result)
    
    # EXIT (NECESSAIRE ?)
    # session.get(current_app.config["TLCEXAM_URL"] + "/summary_list?exit_page=1")

    remove_exam_from_user()
    return True

def open_exam(exam_code: str):
    # session = new_tlc_session()
    # if not session: return None

    ## Start exam
    # session.post(current_app.config["TLCEXAM_URL"] + "/test_list", data={"take_test": exam_code})
        # load_questions
        # show_features
        # show_timed
    # response = session.get(current_app.config["TLCEXAM_URL"] + "/display_question")
    with open("C:\\Users\\Frantkich\\Documents\\Syncordis\\texam\\display_question.htm", "r") as file:
        html_content = file.read()
    soup = bs4.BeautifulSoup(html_content, "html.parser")
    # ^^^^ change that 
    index_start_nb_questions = html_content.find("Question 1 of ")
    index_end_nb_questions = html_content.find("\n", index_start_nb_questions + 1)
    nb_questions = int(html_content[index_start_nb_questions + 13:index_end_nb_questions])
    print(f"Number of questions: '{nb_questions}'")
    return soup, nb_questions
