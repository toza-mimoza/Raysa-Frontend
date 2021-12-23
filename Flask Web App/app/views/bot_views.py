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
            "name": qbot.name,
        }
        bots_list.append(bot)

    return render_template('bots.html', bots_list)
