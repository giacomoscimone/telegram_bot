import os
from dotenv import load_dotenv

import telebot
from telebot.types import Message

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

PATH = "C:\\Users\\Alternanza\\Documents\\GitHub\\telegram_bot\\"


@bot.message_handler(commands=['carica_foto'])
def foto(message: Message):
    bot.reply_to(message, "seleziona la foto: ")
    bot.register_next_step_handler(message=message, callback=upload_foto)


def save_image(img,path):
    with open(path, 'wb') as file:
        file.write(img)


def upload_foto(message: Message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    save_image(downloaded_file, PATH + file_info.file_path[6:])
    bot.reply_to(message, "immagine caricata con successo")


bot.infinity_polling()
