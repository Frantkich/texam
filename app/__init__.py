from flask import Flask
from flask_login import LoginManager
import json


from app.tools.config import configs
import app.tools.db as db
from app.tools.db import Users, Exams


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
        db.db_c.create_all()
        if not db.Users.query.all(): db.db_c.session.add(Users(email='1@1.1', password='1'))
        if not db.Exams.query.all(): db.db_c.session.add(Exams(name='CH1PMB2F', questions=json.loads('[{"description": "FOPM enables a bank to express relationships with a client via","answers": [{"value": "third party","score": 10},{"value": "third party with client_f=1","score": 7},{"value": "Both","score": 0},{"value": "None","score": 1}]},{"description": "What is true about the future cashflow page?","answers": [{"value": "It shows the cash movements in the cash account.","score": 8},{"value": "It projects the dividend payments due to be received on a cash account","score": 8},{"value": "It projects the redemption proceeds due","score": 3},{"value": "B and C","score": 1}]}]')))
        db.db_c.session.commit()

    # Register blueprints 
    # Errors
    from app.views.error import page_not_found, unauthorized
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(401, unauthorized)
    # Routes
    from app.views import admin, frontend, user, exam
    app.register_blueprint(admin.routes)
    app.register_blueprint(frontend.routes)
    app.register_blueprint(user.routes)
    app.register_blueprint(exam.routes)
    return app


@login_manager.user_loader
def user_loader(id):
    return db.Users.query.filter_by(id=id).first()
