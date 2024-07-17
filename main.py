import os
from dotenv import load_dotenv
from server_utils import predict_server
from telebot.types import Message
from costant_path import SAVE_PATH, PATH, LOG_PATH
from io_utils import create_save_location, save_image
import telebot
from logger_utils import setuplog

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)


def upload_foto(message: Message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    save_image(downloaded_file, PATH + file_info.file_path[6:])
    bot.reply_to(message, "immagine caricata con successo")

    classe, confidence = predict_server(file_info.file_path[6:])
    if classe is not None:
        bot.reply_to(message, f"E' una {classe}!\n(Sono sicuro al {round(confidence*100)}%)")


@bot.message_handler(commands=['predizione'])
def class_prediction(message: Message):

    bot.reply_to(message, "seleziona la foto: ")
    bot.register_next_step_handler(message=message, callback=upload_foto)


if __name__ == "__main__":
    create_save_location(SAVE_PATH)
    setuplog(LOG_PATH)
    bot.infinity_polling()
