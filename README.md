# texam

install the matching mysql / python connector

build DB:

```
CREATE DATABASE texam;
CREATE USER syncordian;
GRANT ALL PRIVILEGES ON texam.* TO syncordian;
FLUSH PRIVILEGES;
```

run `> pip install -r requirements.txt`

run `> flask --app main:create_app run --reload --debug`
