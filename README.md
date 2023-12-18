# texam

install the matching mysql / python connector

build DB:

```
CREATE DATABASE texam;
CREATE USER syncordian;
GRANT ALL PRIVILEGES ON texam.* TO syncordian;
FLUSH PRIVILEGES;
USE texam
CREATE TABLE users ( id INT, email VARCHAR(255), password VARCHAR(255) );
INSERT INTO users value (1, 1@1.1, 1);
```

run `> pip install -r requirements.txt`

run `> flask --app main:create_app run --reload --debug`
