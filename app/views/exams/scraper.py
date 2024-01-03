from flask import current_app
from flask_login import current_user
from requests import Session
import bs4

from app.tools.db import remove_exam_from_user, add_exam_questions, assign_exam_to_user, bind_question_to_user, get_question_in_exam


def new_tlc_session() -> Session:
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
    session = new_tlc_session()
    if not session: return None
    
    response = session.get(current_app.config["TLCEXAM_URL"] + "/test_list")
    soup = bs4.BeautifulSoup(response.content, "html.parser")

    exams = []
    for row in soup.find_all("tr")[1:]:
        col = row.find_all("td")
        exams.append({
            "code": col[0].find("input")['value'],
            "name": col[1].text,
            "description": col[2].text,
            "class_name": col[3].text
        })
    return exams


def load_questions(exam_code: str):
    session = new_tlc_session()
    if not session: return None
    session.post(current_app.config["TLCEXAM_URL"] + "/test_list", data={"take_test": exam_code})
    response = session.get(current_app.config["TLCEXAM_URL"] + "/display_question")
    soup = bs4.BeautifulSoup(response.content, "html.parser")
    index_start_nb_questions = response.content.find("Question 1 of ")
    index_end_nb_questions = response.content.find("\n", index_start_nb_questions + 1)
    nb_questions = int(response.content[index_start_nb_questions + 13:index_end_nb_questions])
    print(f"Number of questions: '{nb_questions}'")
    assign_exam_to_user(exam_code)
    for _ in range(nb_questions):
        question_text = soup.find(id="questiontext").text
        print(f"Question: '{question_text}'")
        question = get_question_in_exam(current_user.exam_id, question_text)
        if question:
            bind_question_to_user(question)
        else:
            exam = add_exam_questions(exam_code, [{
                "description": question_text,
                "answers": [{"description": tr.find_all("td")[-1].text} for tr in soup.find_all("tr")[1:]]
            }])
            bind_question_to_user(exam.questions[-1])
    return True


def answering_questions() -> str:
    session = new_tlc_session()
    if not session: return None
    response = session.get(current_app.config["TLCEXAM_URL"] + "/display_question")
    soup = bs4.BeautifulSoup(response.content, "html.parser")
    index_start_nb_questions = response.content.find("Question 1 of ")
    index_end_nb_questions = response.content.find("\n", index_start_nb_questions + 1)
    nb_questions = int(response.content[index_start_nb_questions + 13:index_end_nb_questions])
    for _ in range(nb_questions):
        question_text = soup.find(id="questiontext").text
        question = get_question_in_exam(current_user.exam_id, question_text)
        if not question: return 500 # LA QUESTION NE S'EST PAS BIEN ENREGISTREE
        stop = False
        for index, tr in enumerate(soup.find_all("tr")[1:]):
            for answer in question.answers:
                if answer.description == tr.find_all("td")[-1].text:
                    if answer.score == 2 or answer.score == 3:
                        response = session.post(current_app.config["TLCEXAM_URL"] + "/display_question", data={
                            "cmd": "",
                            "next_ques": "Next>",
                            "taker_ans": index
                        })
                        soup = bs4.BeautifulSoup(response.content, "html.parser")
                        tr.find("input")['checked'] = True
                        if answer.score == 3: stop = True
                    break
            if stop: break
    return generate_report()


def generate_report(fresh_start: bool = False) -> str:
    if fresh_start:
        session = new_tlc_session()
        if not session: return None
    response = session.get(current_app.config["TLCEXAM_URL"] + "/display_question")
    soup = bs4.BeautifulSoup(response.content, "html.parser")
    unanswered = sum([1 for row in soup.find_all('tr')[1:] if row.find_all('td')[3].text != "Answered"])
    question_count = len(soup.find_all('tr')[1:])
    answered_ratio = abs(((unanswered * 100) / question_count) - 100)
    return f"{answered_ratio}% of exam's responses answered."


def submit_exam():
    session = new_tlc_session()
    if not session: return None
    response = session.post(current_app.config["TLCEXAM_URL"] + "/summary_list", data={
        "done": "Finished+taking+Test",
        "curr_screen": "1",
        "skip_buttons": ""
    })
    soup = bs4.BeautifulSoup(response.content, "html.parser")
    result = soup.find_all(class_="metainforight")
    total = result[0].text[13:].split(" ")[0]
    result = result[1].text
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

    # EXIT (NECESSAIRE ?)
    # session.get(current_app.config["TLCEXAM_URL"] + "/summary_list?exit_page=1")
    remove_exam_from_user()
    return detailed_result
