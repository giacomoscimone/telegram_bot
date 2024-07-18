import os
from dotenv import load_dotenv
from server_utils import predict_server
from telebot.types import Message
from constants.paths import SAVE_PATH, LOG_PATH
from io_utils import create_save_location, save_image, clean_up
import telebot
from logger_utils import setuplog
import logging
from commands import start, prediction, menu, help

load_dotenv()

logger = logging.getLogger('my_logger')

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)


def upload_foto(message: Message) -> None:

    if isinstance(message.text, str):
        bot.reply_to(message, "il messaggio inviato non e' una foto")
        return None
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    img_path = file_info.file_path

    downloaded_file = bot.download_file(img_path)
    save_image(downloaded_file, SAVE_PATH + img_path[6:])

    bot.reply_to(message, "immagine caricata con successo")
    logger.info(f"immagine salvata in: {SAVE_PATH + img_path[6:]}")

    classe, confidence = predict_server(img_path[6:])
    if classe is not None:
        bot.reply_to(message, f"E' una {classe}!\n(Sono sicuro al {round(confidence*100)}%)")
    else:
        logger.error("errore richiesta del server")
        bot.reply_to(message, "errore server")


@bot.message_handler(commands=[prediction])
def class_prediction(message: Message) -> None:

    bot.reply_to(message, "seleziona la foto: ")
    logger.debug("risposta inviata")
    bot.register_next_step_handler(message=message, callback=upload_foto)


@bot.message_handler(commands=[start])
def start(message: Message):
    logger.debug("comando start")
    bot.reply_to(message, "Benvenuto")
    bot.reply_to(message, menu)


@bot.message_handler(commands=[help])
def start(message: Message):
    bot.reply_to(message, menu)


if __name__ == "__main__":
    create_save_location(SAVE_PATH)
    clean_up(SAVE_PATH)
    setuplog(LOG_PATH)
    bot.infinity_polling()

