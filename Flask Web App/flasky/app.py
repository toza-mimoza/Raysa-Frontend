from flask import Flask, render_template
from flask import request
import json 

app = Flask(__name__)

def check_if_bot_exists(name):
    file = open('bot_data.json')
    data = json.load(file) 

    # bots list 
    bots_list = data["bots"]
    bots_list_names = []
    for bot in bots_list:
        bots_list_names.append(bot["bot_name"])

    #print(bots_list_names)

    if name in bots_list_names: 
        return True
    else: 
        return False

@app.errorhandler(404)
def page_not_found(content_type):
   return render_template('404.html', content_type=content_type)

@app.route('/')
def index():
    '''Displays root URL.'''
#    return '<h1>Hello World!</h1>'
#    user_agent = request.headers.get('User-Agent')
#    return '<p>Your browser is {}</p>'.format(user_agent)
    return render_template('index.html')

@app.route('/user/<username>')
def template_user(username):
    '''Displays user profile.'''
    return render_template('user.html', username=username)

@app.route('/train/<bot_name>')
def train_bot(bot_name):
    '''Sends request to a specific bot to train.'''
    if not check_if_bot_exists(bot_name):
        return page_not_found(bot_name)
    ##return '<h1>Training... {}!</h1>'.format(bot_name)
    return render_template('train.html', bot_name=bot_name)

@app.route('/logs/<bot_name>')
def show_logs(bot_name):
    '''Shows logs page for a specific bot.'''
    if not check_if_bot_exists(bot_name):
        return page_not_found(bot_name)
    ##return '<h1>Logs... {}!</h1>'.format(bot_name)
    return render_template('logs.html', bot_name=bot_name)

@app.route('/conversations/<bot_name>')
def show_conversations(bot_name):
    '''Shows logs page for a specific bot.'''
    if not check_if_bot_exists(bot_name):
        return page_not_found(bot_name)
    ##return '<h1>Logs... {}!</h1>'.format(bot_name)
    return render_template('conversations.html', bot_name=bot_name)

if __name__ == '__main__':
    app.run()
# test comment