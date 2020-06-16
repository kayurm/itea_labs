"""
Kate Yurmanovych
Lesson 11
1) Написать бота-консультанта, который будет собирать информацию с
пользователя (его ФИО, номер телефона, почта, адрес, пожелания).
Записывать сформированную заявку в БД (по желанию SQl/NOSQL).
t.me/kayurmatik_bot
"""

from telebot import TeleBot
from Lesson_11.utilities import queries as q
from .utilities.config import TOKEN

query = q.Query()
bot = TeleBot(TOKEN)
feedback_info = dict()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    msg = bot.reply_to(message.chat.id, "Oh hey there! I'm a friendly bot Kayurmatik. May I get your full name?")
    bot.register_next_step_handler(msg, get_name_step)


@bot.message_handler(content_types=['text'])
def get_name_step(message):
    full_name = message.text
    feedback_info['chat_id'] = message.chat.id
    feedback_info['full_name'] = full_name
    msg = bot.reply_to(message.chat.id, f"It's lovely to meet you, {full_name}!!! Now, what's your phone number?")
    bot.register_next_step_handler(msg, get_phone_step)


@bot.message_handler(content_types=['text'])
def get_phone_step(message):
    feedback_info['phone'] = message.text
    msg = bot.reply_to(message.chat.id, f"Good. What's your email?")
    bot.register_next_step_handler(msg, get_email_step)


@bot.message_handler(content_types=['text'])
def get_email_step(message):
    feedback_info['email'] = message.text
    msg = bot.reply_to(message.chat.id, f"Alrighty, and what's your address?")
    bot.register_next_step_handler(msg, get_address_step)


@bot.message_handler(content_types=['text'])
def get_address_step(message):
    feedback_info['address'] = message.text
    msg = bot.reply_to(message.chat.id, f"Now, finally, leave your feedback or any wishes.")
    bot.register_next_step_handler(msg, get_feedback_step)


@bot.message_handler(content_types=['text'])
def get_feedback_step(message):
    feedback_info['feedback'] = message.text
    print(feedback_info)
    if query.add_feedback(feedback_info):
        bot.send_message(message.chat.id, f"Thank you, your data was recorded and our expert will get back to you asap")
    else:
        bot.send_message(message.chat.id, f"ooops, something went wrong. We'll fix this asap")


bot.polling()
