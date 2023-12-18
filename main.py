from app import create_app as factory_create_app


def create_app(config_name='dev'):
    return factory_create_app(config_name)
