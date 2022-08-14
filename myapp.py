import telebot
import os

from configs import TOKEN, DEBUG, SECRET_KEY
from main import bot
from utils import sent_sms

from flask import Flask, request, render_template, url_for, flash, redirect

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path="")
app.config['SECRET_KEY'] = SECRET_KEY

# this is the entry point
application = app

messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]


@app.route("/" + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode('utf-8'))])
    return "!", 200


@app.route("/setWebhook/")
def hello():
    bot.remove_webhook()
    bot.set_webhook(url="https://welldone.uz/" + TOKEN)
    return "!", 200


@app.route('/sms/', methods=('GET', 'POST'))
def create_sms():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            sent_sms(content, title)
            messages.append({'title': title, 'content': content})
            return redirect(url_for('create_sms'))
    return render_template('sms.html', messages=messages)


@app.route("/")
def main_page():
    return render_template('index.html')


if __name__ == "__main__":
    # app.run()
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
