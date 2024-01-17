from flask import Flask
from flask_login import LoginManager
from pymysql.err import ProgrammingError
from app.tools.config import configs
from app.tools.db.models import db_c, Users


login_manager = LoginManager()

def create_app(config_name) -> Flask:
    app = Flask(
        __name__,
        static_folder=configs[config_name].STATIC_FOLDER,
        template_folder=configs[config_name].TEMPLATE_FOLDER,
    )
    app.config.from_object(configs[config_name])
    login_manager.init_app(app)
    db_c.init_app(app) 
    
    with app.app_context():
        try:
            # raise Exception("recreate db.")
            if not Users.query.all(): minimal_dump(db_c.session)
        except ProgrammingError:
            print("Database not found. Creating database...")
            db_c.create_all()
            db_c.session.commit()
            print("Database created.")
            if not Users.query.all(): minimal_dump(db_c.session)
    # Register blueprints 
    # Errors
    from app.views.error import page_not_found, unauthorized
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(401, unauthorized)
    # Routes
    from app.views import frontend, user, exams, questions, results
    app.register_blueprint(frontend.routes)
    app.register_blueprint(user.routes)
    app.register_blueprint(exams.routes)
    app.register_blueprint(questions.routes)
    app.register_blueprint(results.routes)
    return app


@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()

def minimal_dump(session):
    session.add(Users(email='fguern@syncordisconsulting.com', password='Syncordis0609', is_admin=True))
    users = [["jconnetable@syncordisconsulting.com", "TLC2020"],["cherson@syncordisconsulting.com", "TLC2018"],["tnguyencong@syncordisconsulting.com", "TLC@2017"],["ffranchet@syncordisconsulting.com", "TLC2020"],["jkaiffer@syncordisconsulting.com", "TLC2017"],["cguidicelli@syncordisconsulting.com", "TLC2020"],["echamlong@syncordisconsulting.com", "Lenacelia23!"],["pbagnis@syncordisconsulting.com",  "#Mog:mq+1uYY"],["afreiria@syncordisconsulting.com",  "Syncordis@2017"],["lsimosimo@syncordisconsulting.com",  "3Bandjounaise!"],["amoquin@syncordisconsulting.com", "TLC2020"]]
    for user in users: session.add(Users(email=user[0], password=user[1]))
    session.commit()
    print("Admin user created.")
