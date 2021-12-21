from flask import Flask, render_template
from flask import request
from util import  check_if_bot_exists 
from flask_sqlalchemy import SQLAlchemy
from models import db, Bot
from flask_migrate import Migrate

app = Flask(__name__)


POSTGRES = {
 'user': 'postgres',
 'pw': 'kill998',
 'db': 'raysadb',
 'host': 'localhost',
 'port': '5432',
}
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
# to suppress warnings for tracking modifications in db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)
#with app.app_context():
#    db.create_all()

@app.errorhandler(404)
def page_not_found(content_name):
    '''
    Returns 404 Page Not Found Custom Error page.
    content_type: Type of content not found (bot, conversation, etc.)
    '''
    return render_template('404.html', content_name=content_name), 404

@app.errorhandler(500)
def internal_server_error(e):
    '''
    Returns 500 Internal Server Error page.
    '''
    return render_template('500.html'), 500

@app.route('/')
def index():
    '''Returns a template for the index page.'''
#    return '<h1>Hello World!</h1>'
#    user_agent = request.headers.get('User-Agent')
#    return '<p>Your browser is {}</p>'.format(user_agent)
    return render_template('index.html')

@app.route('/user/<username>')
def template_user(username):
    '''Returns a template for the user profile page.'''
    return render_template('user.html', username=username)

@app.route('/train/<bot_name>')
def train_bot(bot_name):
    '''Returns a template for training overview for a specific bot.'''
    if not check_if_bot_exists(bot_name):
        return page_not_found(bot_name)
    ##return '<h1>Training... {}!</h1>'.format(bot_name)
    return render_template('train.html', bot_name=bot_name)

@app.route('/logs/<bot_name>')
def show_logs(bot_name):
    '''Returns a template for logs overview for a specific bot.'''
    if not check_if_bot_exists(bot_name):
        return page_not_found(bot_name)
    ##return '<h1>Logs... {}!</h1>'.format(bot_name)
    return render_template('logs.html', bot_name=bot_name)

@app.route('/conversations/<bot_name>')
def show_all_conversations(bot_name):
    '''Returns a template for conversations overview for a specific bot.'''
    if not check_if_bot_exists(bot_name):
        return page_not_found(bot_name)

    return render_template('conversations.html', bot_name=bot_name)

@app.route('/statistics/all')
def show_statistics_for_all():
    '''Returns a template for conversations overview for a specific bot.'''

    # get all bots from db
    # get all bots from json
    result = Bot(1, "Bot1")
    db.session.add(result)
    db.session.commit()
 
    return render_template('stats_all.html')

@app.route('/statistics/<bot_name>')
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

if __name__ == '__main__':
    app.run()