from app import create_app as factory_create_app


app = factory_create_app()

def create_app():
    return app
