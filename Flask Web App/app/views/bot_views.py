from flask import Blueprint, redirect, render_template
from flask import request, url_for
from flask_user import current_user, login_required, roles_required
from flask import Response
from time import sleep
from app import db

from app.models.bot_models import Bots
from app.views.error_views import page_not_found, internal_server_error
from app.util import check_if_bot_exists 
from pygtail import Pygtail
import time 
bot_blueprint = Blueprint('bot', __name__, template_folder='templates')

LOG_FILE = 'logs/Art Chatbot.log'
# log = logging.getLogger('__name__')
# logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)


@bot_blueprint.route('/bots')
def index():
    '''Returns a template for the index page.'''
    #    return '<h1>Hello World!</h1>'
    #    user_agent = request.headers.get('User-Agent')
    #    return '<p>Your browser is {}</p>'.format(user_agent)
    bots_list = []

    for qbot in Bots.query.all(): 
        bots_list.append(qbot)

    return render_template('bots.html', bots_list=bots_list)

@bot_blueprint.route('/train/<bot_name>')
@roles_required('Admin')  # Limits access to users with the 'admin' role
def train_bot(bot_name):
    '''Returns a template for training overview for a specific bot.'''
    if not check_if_bot_exists(bot_name):
        return page_not_found(bot_name)
        
    bot = Bots.query.filter_by(bot_name = bot_name).first()

    return render_template('bots/train.html', bot=bot)

@bot_blueprint.route('/logs/<bot_name>')
@roles_required('Admin')  # Limits access to users with the 'admin' role
def show_logs(bot_name):
    '''Returns a template for logs overview for a specific bot.'''
    if not check_if_bot_exists(bot_name):
        return page_not_found(bot_name)
    
    bot = Bots.query.filter_by(bot_name = bot_name).first()

    return render_template('bots/logs.html', bot=bot)

@bot_blueprint.route('/')
def entry_point():
	# log.info("route =>'/env' - hit!")
	return render_template('bots/logs.html')


@bot_blueprint.route('/progress')
def progress():
    def generate():
        x = 0
        while x <= 100:
            yield "data:" + str(x) + "\n\n"
            x = x + 10
            time.sleep(0.5)
    return Response(generate(), mimetype= 'text/event-stream')


@bot_blueprint.route('/log')
def progress_log():
	def generate():
		for line in Pygtail(LOG_FILE, every_n=1):
			yield "data:" + str(line) + "\n\n"
			time.sleep(1)
	return Response(generate(), mimetype= 'text/event-stream')


@bot_blueprint.route('/env')
def show_env():
	# log.info("route =>'/env' - hit")
	env = {}
	for k,v in request.environ.items(): 
		env[k] = str(v)
	# log.info("route =>'/env' [env]:\n%s" % env)
	return env

@bot_blueprint.route('/conversations/<bot_name>')
@login_required  # Limits access to authenticated users
def show_all_conversations(bot_name):
    '''Returns a template for conversations overview for a specific bot.'''
    if not check_if_bot_exists(bot_name):
        return page_not_found(bot_name)

    return render_template('bots/conversations.html', bot_name=bot_name)

@bot_blueprint.route('/statistics/all')
@login_required  # Limits access to authenticated users
def show_statistics_for_all():
    '''Returns a template for conversations overview for a specific bot.'''

    # get all bots from db
 
    return render_template('bots/stats_all.html')

@bot_blueprint.route('/statistics/<bot_name>')
def show_statistics_for_bot(bot_name):
    '''Returns a template for conversations overview for a specific bot.'''
    if not check_if_bot_exists(bot_name):
        return page_not_found(bot_name)

    # retrieve bot information from db

    context = {
        "bot_name": "REPLACE", 
        "cluster_name": "REPLACE"
    }      
    return render_template('bots/stats_bot.html', **context)
