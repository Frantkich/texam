from flask import Flask, Blueprint
from flask_login import LoginManager
from pymysql.err import ProgrammingError
from app.tools.config import configs
from app.tools.db.models import db_c, Users


login_manager = LoginManager()

def create_app(config_name="config") -> Flask:
    app = Flask(
        __name__,
        static_folder=configs[config_name].STATIC_FOLDER,
        template_folder=configs[config_name].TEMPLATE_FOLDER,
        static_url_path=f'/{configs[config_name].PROJECT_NAME}/static'
    )
    app.config.from_object(configs[config_name])
    login_manager.init_app(app)
    db_c.init_app(app) 
    
    with app.app_context():
        try:
            # raise Exception(ProgrammingError)
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
    main_bp = Blueprint('main', __name__, url_prefix=f"/{configs[config_name].PROJECT_NAME}")
    from app.views import frontend, user, exams, questions, results, admin
    main_bp.register_blueprint(frontend.routes)
    main_bp.register_blueprint(user.routes)
    main_bp.register_blueprint(exams.routes)
    main_bp.register_blueprint(questions.routes)
    main_bp.register_blueprint(results.routes)
    main_bp.register_blueprint(admin.routes)
    app.register_blueprint(main_bp)
    return app


@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()

def minimal_dump(session):
    session.add(Users(email='fguern@syncordisconsulting.com', password='Syncordis0609', role=1))
    users = [["jconnetable@syncordisconsulting.com", "TLC2020"],["cherson@syncordisconsulting.com", "TLC2018"],["tnguyencong@syncordisconsulting.com", "TLC@2017"],["ffranchet@syncordisconsulting.com", "TLC2020"],["jkaiffer@syncordisconsulting.com", "TLC2017"],["cguidicelli@syncordisconsulting.com", "TLC2020"],["echamlong@syncordisconsulting.com", "Lenacelia23!"],["pbagnis@syncordisconsulting.com",  "#Mog:mq+1uYY"],["afreiria@syncordisconsulting.com",  "Syncordis@2017"],["lsimosimo@syncordisconsulting.com",  "3Bandjounaise!"],["amoquin@syncordisconsulting.com", "TLC2020"]]
    session.commit()
    print("Admin user created.")
