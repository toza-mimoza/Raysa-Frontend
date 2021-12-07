from flask import Flask, render_template
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
#    return '<h1>Hello World!</h1>'
#    user_agent = request.headers.get('User-Agent')
#    return '<p>Your browser is {}</p>'.format(user_agent)
    return render_template('index.html')

@app.route('/user/<name>')
def template_user(name):
    return render_template('user.html', name=name)


#@app.route('/user/<user_name>')
#def user(user_name):
#    return '<h1>Hello, {}!</h1>'.format(user_name)

@app.route('/bot/train/<bot_name>')
def train_bot(bot_name):
    '''Sends request to a specific bot to train.'''
    return '<h1>Training... {}!</h1>'.format(bot_name)

@app.route('/bot/logs/<bot_name>')
def show_logs(bot_name):
    '''Shows logs page for a specific bot.'''
    return '<h1>Logs... {}!</h1>'.format(bot_name)

if __name__ == '__main__':
    app.run()