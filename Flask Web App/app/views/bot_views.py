from flask import Blueprint, redirect, render_template
from flask import request, url_for
from flask_user import current_user, login_required, roles_required

from app import db
from app.models.user_models import UserProfileForm, UserRegisterForm
from app.models.bot_models import Bot
from app.util import check_if_bot_exists 

bot_blueprint = Blueprint('bot', __name__, template_folder='templates')

@bot_blueprint.app_errorhandler(404)
def page_not_found(content_name):
    '''
    Returns 404 Page Not Found Custom Error page.
    content_name: Type of content not found (bot, conversation, etc.)
    '''
    return render_template('404.html', content_name=content_name), 404

@bot_blueprint.app_errorhandler(500)
def internal_server_error(e):
    '''
    Returns 500 Internal Server Error page.
    '''
    return render_template('500.html'), 500

@bot_blueprint.route('/bots')
def index():
    '''Returns a template for the index page.'''
#    return '<h1>Hello World!</h1>'
#    user_agent = request.headers.get('User-Agent')
#    return '<p>Your browser is {}</p>'.format(user_agent)
    bots_list = []

    for qbot in Bot.query.all(): 

        bot = {
            "bot_name": qbot.bot_name,
            "bot_description": qbot.bot_description,
            "bot_added_at": qbot.bot_added_at,
            "vm_name": qbot.vm_name,
            "vm_res_group": qbot.vm_res_group,
            "vm_type": qbot.vm_type,
            "vm_ip": qbot.vm_ip,
            "vm_vcpu": qbot.vm_vcpu,
            "vm_region": qbot.vm_region,
            "vm_ram": qbot.vm_ram,
        }
        bots_list.append(bot)

    return render_template('bots.html', bots_list=bots_list)

@bot_blueprint.route('/train/<bot_name>')
@roles_required('Admin')  # Limits access to users with the 'admin' role
def train_bot(bot_name):
    '''Returns a template for training overview for a specific bot.'''
    if not check_if_bot_exists(bot_name):
        return page_not_found(bot_name)
    ##return '<h1>Training... {}!</h1>'.format(bot_name)
    return render_template('train.html', bot_name=bot_name)

@bot_blueprint.route('/logs/<bot_name>')
@roles_required('Admin')  # Limits access to users with the 'admin' role
def show_logs(bot_name):
    '''Returns a template for logs overview for a specific bot.'''
    if not check_if_bot_exists(bot_name):
        return page_not_found(bot_name)
    ##return '<h1>Logs... {}!</h1>'.format(bot_name)
    return render_template('logs.html', bot_name=bot_name)

@bot_blueprint.route('/conversations/<bot_name>')
@login_required  # Limits access to authenticated users
def show_all_conversations(bot_name):
    '''Returns a template for conversations overview for a specific bot.'''
    if not check_if_bot_exists(bot_name):
        return page_not_found(bot_name)

    return render_template('conversations.html', bot_name=bot_name)

@bot_blueprint.route('/statistics/all')
@login_required  # Limits access to authenticated users
def show_statistics_for_all():
    '''Returns a template for conversations overview for a specific bot.'''

    # get all bots from db
    # get all bots from json
 
    return render_template('stats_all.html')

@bot_blueprint.route('/statistics/<bot_name>')
def show_statistics_for_bot(bot_name):
    '''Returns a template for conversations overview for a specific bot.'''
    if not check_if_bot_exists(bot_name):
        return page_not_found(bot_name)

    # retrieve bot information from db
    # retrieve bot information from json file 

    context = {
        "bot_name": "REPLACE", 
        "cluster_name": "REPLACE"
    }      
    return render_template('stats_bot.html', **context)
