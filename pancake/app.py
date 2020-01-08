from flask import Flask

from pancake.routes import pancakes


def create_app(config_object):
    """
    Factory for creating api using provided configuration object.
    """
    app = Flask('GlowingPancake', static_url_path='/static')
    app.config.from_object(config_object)
    register_blueprints(app)
    return app


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(pancakes.blueprint)
