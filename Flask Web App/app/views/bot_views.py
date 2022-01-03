from flask import Blueprint, render_template
from flask import request
from flask_user import login_required, roles_required
from flask import Response

from app.models.bot_models import Bots, Statistics

from app.views.error_views import page_not_found
from app.util import check_if_bot_exists
from pygtail import Pygtail
import time

bot_blueprint = Blueprint("bot", __name__, template_folder="templates")

LOG_FILE = "logs/Art Chatbot.log"


@bot_blueprint.route("/bots")
def show_all_bots():
    """Returns a template for the show_all_bots page."""
    bots_list = []

    for qbot in Bots.query.all():
        bots_list.append(qbot)

    return render_template("bots/bots.html", bots_list=bots_list)


@bot_blueprint.route("/train/<bot_name>")
@roles_required("Admin")  # Limits access to users with the 'admin' role
def train_bot(bot_name):
    """Returns a template for training overview for a specific bot."""
    if not check_if_bot_exists(bot_name):
        return page_not_found(bot_name)

    bot = Bots.query.filter_by(bot_name=bot_name).first()

    return render_template("bots/train.html", bot=bot)


@bot_blueprint.route("/logs/<bot_name>")
@roles_required("Admin")  # Limits access to users with the 'admin' role
def show_logs(bot_name):
    """Returns a template for logs overview for a specific bot."""
    if not check_if_bot_exists(bot_name):
        return page_not_found(bot_name)

    bot = Bots.query.filter_by(bot_name=bot_name).first()

    return render_template("bots/logs.html", bot=bot)


@bot_blueprint.route("/")
def entry_point():
    return render_template("bots/logs.html")


@bot_blueprint.route("/progress")
def progress():
    def generate():
        x = 0
        while x <= 100:
            yield "data:" + str(x) + "\n\n"
            x = x + 10
            time.sleep(0.5)

    return Response(generate(), mimetype="text/event-stream")


@bot_blueprint.route("/log")
def progress_log():
    def generate():
        for line in Pygtail(LOG_FILE, every_n=1):
            yield "data:" + str(line) + "\n\n"
            time.sleep(1)

    return Response(generate(), mimetype="text/event-stream")


@bot_blueprint.route("/env")
def show_env():
    env = {}
    for k, v in request.environ.items():
        env[k] = str(v)
    return env


@bot_blueprint.route("/conversations/<bot_name>")
@login_required  # Limits access to authenticated users
def show_all_conversations(bot_name):
    """Returns a template for conversations overview for a specific bot."""
    if not check_if_bot_exists(bot_name):
        return page_not_found(bot_name)

    return render_template("bots/conversations.html", bot_name=bot_name)


@bot_blueprint.route("/statistics/all")
@login_required  # Limits access to authenticated users
def show_statistics_for_all():
    """Returns a template for conversations overview for a specific bot."""

    # get all bots from db

    bot_stats_list = Statistics.query.all()

    return render_template("bots/stats_all.html", bot_stats_list=bot_stats_list)


@bot_blueprint.route("/statistics/<bot_name>")
def show_statistics_for_bot(bot_name):
    """Returns a template for conversations overview for a specific bot."""
    if not check_if_bot_exists(bot_name):
        return page_not_found(bot_name)

    # retrieve bot information from db

    context = {"bot_name": "REPLACE", "cluster_name": "REPLACE"}
    return render_template("bots/stats_bot.html", **context)
