# texam

Small app to create quizz to prepare to temenos exams.

it includes RBAC to quizz, synchronisation to real serveur, scraping of questions, aggreagation of all user answers if needed, verification and much more...

## WIP

The app is not fully finished/polished

But i don´t have enough time to continue this project.



## Installation

install the matching mysql / python connector

build DB:

```
CREATE DATABASE texam;
CREATE USER syncordian;
GRANT ALL PRIVILEGES ON texam.* TO syncordian;
FLUSH PRIVILEGES;
```

run `> venv/bin/pip install -r requirements.txt`

## run dev server

You might need to change the db address > app\tools\config.py

run `> <PATH TO FLASK> --app main:create_app run --reload --debug`

run prod server

run `> venv/bin/gunicorn -w 2 'main:app'`
