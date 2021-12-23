from .main_views import main_blueprint
from .bot_views import bot_blueprint

def register_blueprints(app):
    app.register_blueprint(main_blueprint)
    app.register_blueprint(bot_blueprint)