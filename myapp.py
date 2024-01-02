import telebot
import os
import json

from telebot import formatting

from configs import TOKEN, DEBUG, SECRET_KEY
from main import bot
from utils import sent_sms

from flask import Flask, request, render_template, url_for, flash, redirect, jsonify

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path="")
app.config['SECRET_KEY'] = SECRET_KEY

# this is the entry point
application = app

messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]


@app.context_processor
def inject_debug():
    return dict(debug=app.debug)


@app.route("/arashbot/" + TOKEN, methods=['POST'])
def getMessage():
    x = request.stream.read().decode('utf-8')
    bot.send_message(390736292, formatting.mcode(str(json.loads(x))), parse_mode='MarkdownV2')
    bot.process_new_updates([telebot.types.Update.de_json(x)])
    return "!", 200


@app.route("/setWebhook/")
def hello():
    bot.remove_webhook()
    bot.set_webhook(url="https://welldone.uz/arashbot/" + TOKEN)
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
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip = request.environ['REMOTE_ADDR']
    else:
        ip = request.environ['HTTP_X_FORWARDED_FOR']
    bot.send_message(390736292, f"Site run with ip: {ip}")
    return render_template('index.html')


@app.route('/ip/', methods=['GET'])
def get_tasks():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return jsonify({'ip': request.environ['REMOTE_ADDR']}), 200
    else:
        return jsonify({'ip': request.environ['HTTP_X_FORWARDED_FOR']}), 200

if __name__ == "__main__":
    # app.run(debug=DEBUG)  # for testing
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8090)),
            debug=DEBUG)  # for production
