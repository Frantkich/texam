# from app import create_app as factory_create_app

# def create_app(config_name='dev'):
#     return factory_create_app(config_name)

# Connect to the database
from sqlalchemy import create_engine
from sqlalchemy import text

engine = create_engine('mysql://syncordian@frantkich.fr:3306/texam')

with engine.connect() as connection:
    result = connection.execute(text("select username from users"))
    for row in result:
        print("username:", row.username)
# engine = create_engine("mysql+mysqldb://syncordian@frantkich.fr/texam")