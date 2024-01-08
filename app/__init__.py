from flask import Flask
from flask_login import LoginManager

from app.tools.config import configs
import app.tools.db as db
from app.tools.db import Users


login_manager = LoginManager()

def create_app(config_name) -> Flask:
    app = Flask(
        __name__,
        static_folder=configs[config_name].STATIC_FOLDER,
        template_folder=configs[config_name].TEMPLATE_FOLDER,
    )
    app.config.from_object(configs[config_name])
    login_manager.init_app(app)
    db.db_c.init_app(app) 
    
    with app.app_context():
        try:
            # raise Exception("recreate db.")
            if not db.Users.query.all(): create_admin(db.db_c.session)
        except Exception as e:
            print(e)
            db.db_c.create_all()
            db.db_c.session.commit()
            print("Database created.")
            if not db.Users.query.all(): create_admin(db.db_c.session)
    # Register blueprints 
    # Errors
    from app.views.error import page_not_found, unauthorized
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(401, unauthorized)
    # Routes
    from app.views import admin, frontend, user, exams, questions, results
    app.register_blueprint(admin.routes)
    app.register_blueprint(frontend.routes)
    app.register_blueprint(user.routes)
    app.register_blueprint(exams.routes)
    app.register_blueprint(questions.routes)
    app.register_blueprint(results.routes)
    return app


@login_manager.user_loader
def user_loader(id):
    return db.Users.query.filter_by(id=id).first()

def create_admin(session):
    session.add(Users(email='fguern@syncordisconsulting.com', password='Syncordis0609', is_admin=True))
    session.commit()
    print("Admin user created.")