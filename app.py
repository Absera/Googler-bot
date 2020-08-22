from flask import Flask, request
import telegram
from telebot.credentials import bot_token, bot_user_name,URL
from telebot.main import Google, Word, Lyrics


global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)


google = Google()
word = Word()
lyrics = Lyrics()


@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    text = update.message.text.encode('utf-8').decode()
    text_list = text.split(" ")
    command = text_list[0]
    formatted = " ".join(text_list[1:])
    bot.sendMessage(chat_id=chat_id, text="WELCOME")

    if command == "/start":
        bot.sendMessage(chat_id=chat_id, text=formatted, reply_to_message_id=msg_id)
    elif command == "/go":
        bot.sendMessage(chat_id=chat_id, text=formatted, reply_to_message_id=msg_id)
    elif command == "/lyrics":
        bot.sendMessage(chat_id=chat_id, text="Lyricsing...", reply_to_message_id=msg_id)
    elif command == "/dict":
        bot.sendMessage(chat_id=chat_id, text="Translating...", reply_to_message_id=msg_id)
    else:
        bot.sendMessage(chat_id=chat_id, text="Please Enter Valid Command!", reply_to_message_id=msg_id)

    return 'ok'


@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook(f'{URL}{TOKEN}')
    if s: return "webhook setup ok"
    else: return "webhook setup failed"


@app.route('/')
def index():
    return '.'


if __name__ == '__main__':
    app.run(threaded=True)