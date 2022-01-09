from flask import Blueprint, render_template
from flask import request, json
from flask_user import login_required, roles_required
from flask import Response

from app.models.bot_models import Bots, Statistics

from app.views.error_views import page_not_found
from app.util.util import check_if_bot_exists
from pygtail import Pygtail
import time
import logging

bot_blueprint = Blueprint("bot", __name__, template_folder="templates")
log = logging.getLogger(__name__)

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
    bots_list = Bots.query.all()

    weekday_code_dict = {
        0: "Mon",
        1: "Tue",
        2: "Wed",
        3: "Thu",
        4: "Fri",
        5: "Sat",
        6: "Sun",
    }
    bot_data = []
    bot_labels = []
    # get past seven days of stats data for a bot
    if not bots_list:
        log.critical("No bots in DB, function cannot proceed.")
    for bot in bots_list:
        stats_objs = Statistics.retrieve_past_week(bot_id=bot.id)
        if stats_objs:
            temp_list_data = []
            temp_list_labels = []
            for stats in stats_objs:
                temp_list_data.append(stats.num_requests_handled)
                date = stats.date_added
                weekday_verbose = weekday_code_dict[stats.date_added.weekday()]
                label_temp = f"{weekday_verbose}, {date.day}.{date.month}.{date.year}"
                temp_list_labels.append(label_temp)
            bot_data.append(temp_list_data)
            bot_labels.append(temp_list_labels)
            log.info(f"Statistics object for bot: {bot.bot_name} found!")
        else:
            log.warn(f"Statistics object for bot: {bot.bot_name} not found!")
            pass
    return render_template(
        "bots/stats_all.html", data=bot_data, labels=bot_labels, bots_list=bots_list
    )


@bot_blueprint.route("/statistics/<bot_name>")
def show_statistics_for_bot(bot_name):
    """Returns a template for conversations overview for a specific bot."""
    if not check_if_bot_exists(bot_name):
        return page_not_found(bot_name)

    # retrieve bot information from db

    context = {"bot_name": "REPLACE", "cluster_name": "REPLACE"}
    return render_template("bots/stats_bot.html", **context)
