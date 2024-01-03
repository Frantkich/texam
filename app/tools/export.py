def export():
    import os
    import json
    from app.tools.db import add_exam_questions, Exams
    folder_path = 'app/tools/exports'
    for filename in os.listdir(folder_path):
        try:
            exam_name = filename.split('-')[0].replace(' ', '')
            print(f"File name: {filename}")
            with open(os.path.join(folder_path, filename), 'r') as f: json_file = json.load(f)
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
                questions.append({
                    "description": question["question"],
                    "answers": [{"description": answer} for answer in question["answers"]]
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
