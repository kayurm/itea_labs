"""
Kate Yurmanovych
Lesson 9 Task 1

Создать бот для поиска статей на википедии.
При входе, бот запрашивает пользователя ввести имя статьи.
Далее бот осуществляет этот поиск на википедии, в случае отстутвия выводит соотвествующие сообщение,
а если статья найдена выводит на экран текст.
"""
from telebot import TeleBot
import wikipedia
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
from config import TOKEN
from Lesson_12.bot_status import Status

status = Status()
bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton(text="Yes")
    button2 = KeyboardButton(text="No")
    kb.add(button1, button2)
    bot.send_message(message.chat.id, "Well, Hello! A friendly bot Kayurmatik here. Shall we do some wiki search?"
                                      "  ->> use buttons below to reply",
                     reply_markup=kb)


@bot.message_handler(content_types=['text'])
def get_name_step(message):
    if message.text in ("No", "no", "stop"):
        bot.send_message(message.chat.id, "Maybe next time then :)")
    elif message.text in ("Yes", "yes", "search"):
        bot.send_message(message.chat.id, "What do you want to search?")
    else:

        button_list = list()
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        search = wikipedia.search(message.text, results=3)
        if search:
            for item in search:
                button_list.append(KeyboardButton(text=item))
            kb.add(button_list[0], button_list[1], button_list[2])
            if status.status == 0:
                bot.send_message(message.chat.id, "Choose one of the articles", reply_markup=kb)
                status.status = 1
            try:
                for item in search:
                    if item == message.text:
                        search_article = wikipedia.page(message.text)
                        if len(search_article.content) > 4096:
                            bot.send_message(message.chat.id,
                                             "The article is too long and it'll be truncated. "
                                             f"To see entire article, follow the link: {search_article.url}")
                        bot.send_message(message.chat.id, search_article.content[:4096])
            except wikipedia.exceptions.DisambiguationError:
                bot.send_message(message.chat.id, "Ooops...got some search disambiguation error from wiki. Try again")
        else:
            bot.send_message(message.chat.id,
                             "Seems like there's no articles related to your search criteria. Try again")


if __name__ == '__main__':
    bot.polling()
