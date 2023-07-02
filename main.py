import os
import requests
from telebot import TeleBot
from telebot import types

BOT_TOKEN = os.environ.get('BOT_TOKEN') 
bot = TeleBot("YOU_KEY")


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    keyboard = types.ReplyKeyboardMarkup(True)
    keyboard.row("Fact")
    bot.send_message(message.chat.id, 'Welcome. You can get a random fact simply by pressing the button!', reply_markup=keyboard)

def print_random_fact(chat_id: int):
    url = "https://uselessfacts.jsph.pl/api/v2/facts/random"
    response = requests.get(url)
    bot.send_message(chat_id, response.json()["text"])

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'fact':
        print_random_fact(message.chat.id)
        

bot.infinity_polling()