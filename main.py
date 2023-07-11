import os
import threading
import requests
from telebot import TeleBot
from telebot import types
import mongo_service
import constants

import schedule
import time

BOT_TOKEN = os.environ.get('BOT_TOKEN') 
bot = TeleBot(constants.BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    keyboard = types.ReplyKeyboardMarkup(True)
    keyboard.row("Fact")
    keyboard.row("Subscribe")
    bot.send_message(message.chat.id, 'Welcome. You can get a random fact simply by pressing the button!', reply_markup=keyboard)

def print_random_fact(chat_id: int):
    url = "https://uselessfacts.jsph.pl/api/v2/facts/random"
    response = requests.get(url)
    bot.send_message(chat_id, response.json()["text"])

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'fact':
        print_random_fact(message.chat.id)
    elif message.text.lower() == 'subscribe':
        subscribe(message.chat.id, message.from_user.username)

def subscribe(chat_id: int, username: str):
    mongo_service.upload_user(chat_id, username)
    bot.send_message(chat_id,"Thank you for subscription")


def send_scheduled_messages():
    users = mongo_service.get_users_from_db()
    for user in users:
        chat_id = user['_id']
        bot.send_message(chat_id,"Fact of the day:")
        print_random_fact(chat_id)
    

schedule.every().day.at(constants.SEND_MESSAGE_TIME).do(send_scheduled_messages)

def run_time_check():
    while True:
        schedule.run_pending()
        time.sleep(1)

thread = threading.Thread(target=run_time_check)
thread.start()

bot.infinity_polling()