
import os
import json
from app.tools.db import add_exam_questions, Exams

FOLDER_PATH = 'app/tools/exports'

def export_questions():
    for filename in os.listdir(FOLDER_PATH):
        try:
            exam_name = filename.split('-')[0].replace(' ', '')
            print(f"File name: {filename}")
            with open(os.path.join(FOLDER_PATH, filename), 'r') as f: json_file = json.load(f)
            if not "Questions" in json_file:
                print(f"No questions found.")
                continue
            exam = Exams.query.filter(Exams.name.like(f"%{exam_name}%")).first()
            if exam: exam_code = exam.code
            else:
                print(f"Exam not found.")
                continue
            questions = []
            for question in json_file["Questions"]:
                correctResponse = question["correctResponse"] if "correctResponse" in question else None
                otherResponses = question["response"] if "response" in question else None
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
                    if otherResponses and answer_value == otherResponses: answer["score"] = 2
                    if correctResponse and answer_value == correctResponse: answer["score"] = 3
                    if "score" in answer and answer["score"] > 1: answer["remarks"] = remarks
                    answers.append(answer)
                questions.append({
                    "description": question["question"],
                    "answers": answers
                })
            if not questions:
                print(f"No questions found.")
                continue
            print(f"Sending {len(questions)} questons...")
            add_exam_questions(exam_code, questions)
            print(f"Questions sent.")
        except Exception as e:
            print(f"Error: {e}")
            continue
