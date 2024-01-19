
import os
import json
from app.tools.db.methods import add_exam_questions
from app.tools.db.models import Exams

FOLDER_PATH = 'app/tools/exports'

def export_questions():
    for filename in os.listdir(FOLDER_PATH):
        try:
            exam_name = filename.split('-')[0].replace(' ', '')
            with open(os.path.join(FOLDER_PATH, filename), 'r') as f: json_file = json.load(f)
            if not "Questions" in json_file:
                print(f"No questions found.")
                continue
            exam = Exams.query.filter(Exams.name.like(f"%{exam_name}%")).first()
            if not exam:
                print(f"Exam not found: {exam_name}")
                continue
            questions = []
            for question in json_file["Questions"]:
                correctResponse = question["correctResponse"] if "correctResponse" in question else None
                otherResponses = question["response"] if "response" in question else None
                if not correctResponse and not otherResponses:
                    continue
                remarks = question["remarque"] if "remarque" in question else None
                if remarks: 
                    remarks = "".join(remarks).replace("\n", "").replace("[", "").replace("]", "")
                    if remarks:
                        if remarks[0] == "'": remarks = remarks[1:]
                        if remarks[-1] == "'": remarks = remarks[:-1]
                if not remarks: remarks = "Add before The Great Export."
                answers = []
                for answer_value in question["answers"]:
                    answer = {"description": answer_value}
                    if answer_value == otherResponses: answer["score"] = 2
                    if answer_value == correctResponse: answer["score"] = 3
                    if "score" in answer: answer["remarks"] = remarks
                    answers.append(answer)
                questions.append({
                    "description": question["question"],
                    "answers": answers
                })
            if not questions:
                continue
            print(f"File name: {filename}")
            print(f"Sending {len(questions)} questions...")
            add_exam_questions(exam.name, questions)
            print(f"Questions sent.")
        except Exception as e:
            print(f"Error: {e}")
            continue
