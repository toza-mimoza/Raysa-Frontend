from flask import Blueprint, render_template
from flask_user import roles_required

from app.views.error_views import page_not_found
from app.models.bot_models import Bots
from app.common.extensions import cache

manager_blueprint = Blueprint("manager", __name__, template_folder="templates")


@manager_blueprint.route("/manager")
@roles_required("Admin")
@cache.cached(timeout=50)
def control_panel():
    """Returns a template for the control panel of the manager."""

    query_bots = Bots.query.all()

    return render_template("manager/manager.html", bots_list=query_bots)


@manager_blueprint.route("/manager/train/<bot_name>")
@roles_required("Admin")  # Limits access to users with the 'admin' role
def train_bot(bot_name):
    """Returns a template for training overview for a specific bot."""

    bot = Bots.query.filter_by(bot_name=bot_name).first()

    if not bot:
        return page_not_found("Bot")
    return render_template("manager/train.html", bot=bot)
