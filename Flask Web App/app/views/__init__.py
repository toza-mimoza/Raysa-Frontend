from .main_views import main_blueprint
from .bot_views import bot_blueprint
from .site_views import site_blueprint
from .error_views import error_blueprint

def register_blueprints(app):
    app.register_blueprint(main_blueprint)
    app.register_blueprint(bot_blueprint)
    app.register_blueprint(site_blueprint)
    app.register_blueprint(error_blueprint)