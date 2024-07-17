import os
from dotenv import load_dotenv

import telebot
from telebot.types import Message

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['carica_foto'])
def foto(message: Message):
    bot.reply_to(message, "seleziona la foto: ")
    bot.register_next_step_handler(message=message, callback=upload_foto)


def save_image(img):
    with open("C:\\Users\\Alternanza\\Documents\\GitHub\\telegram_bot\\foto.jpeg", 'wb') as file:
        file.write(img)


def upload_foto(message: Message):
    image = message.photo[0].file_id
    file_info = bot.get_file(image)
    downloaded_file = bot.download_file(file_info.file_path)
    save_image(downloaded_file)
    bot.reply_to(message, "immagine caricata con successo")


bot.infinity_polling()
