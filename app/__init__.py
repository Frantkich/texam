from flask import Flask
from flask_login import LoginManager


from app.tools.config import configs
import app.tools.db as db


login_manager = LoginManager()

def create_app(config_name):
    app = Flask(
        __name__,
        static_folder=configs[config_name].STATIC_FOLDER,
        template_folder=configs[config_name].TEMPLATE_FOLDER,
    )
    app.config.from_object(configs[config_name])
    login_manager.init_app(app)
    db.db_connector.init_app(app)

    # Register blueprints
    # Errors
    from app.views.error import page_not_found, unauthorized
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(401, unauthorized)
    # Routes
    from app.views import admin, frontend, log
    app.register_blueprint(admin.routes)
    app.register_blueprint(frontend.routes)
    app.register_blueprint(log.routes)
    return app


@login_manager.user_loader
def user_loader(email):
    return return_user(email)

@login_manager.request_loader
def request_loader(request):
    return return_user(request.form.get("email"))

def return_user(email):
    db.get_user(email)
    user = db.User()
    user.id = email
    return user
