import os
import telebot
import logging
from dotenv import load_dotenv
from telebot.types import Message
from constants.paths import SAVE_PATH, LOG_PATH
from io_utils import create_save_location, clean_up
from logger_utils import setuplog
from commands import START, PREDICTION, COMMANDS_LIST, HELP, GRAYSCALE, RESIZE
from upload_utils import upload_foto_resize, upload_foto_predict, upload_foto_grayscale

load_dotenv()

logger = logging.getLogger('my_logger')

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)


def show_menu(chat_id):
    elenco = "\n/".join(COMMANDS_LIST)
    bot.send_message(chat_id, f"Elenco comandi: \n/{elenco}")


@bot.message_handler(commands=[PREDICTION])
def class_prediction(message: Message) -> None:

    bot.reply_to(message, "seleziona la foto: ")
    logger.debug("risposta inviata")
    bot.register_next_step_handler(message=message, callback=upload_foto_predict)


@bot.message_handler(commands=[START])
def start(message: Message):
    logger.debug("comando start")
    bot.reply_to(message, "Benvenuto")
    show_menu(message.chat.id)
    logger.debug("elenco comandi inviato")


@bot.message_handler(commands=[HELP])
def help(message: Message):
    show_menu(message.chat.id)
    logger.debug("elenco comandi inviato")


@bot.message_handler(commands=[GRAYSCALE])
def grayscale(message: Message):
    bot.reply_to(message, "seleziona la foto: ")
    logger.debug("risposta inviata")
    bot.register_next_step_handler(message=message, callback=upload_foto_grayscale)


@bot.message_handler(commands=[RESIZE])
def resize(message: Message):
    try:
        args = message.text.split(" ")[1:]
        altezza = int(args[0])
        larghezza = int(args[1])
    except:
        bot.reply_to(message, "errore nella formulazione del messaggio")
        help(message)
        return None
    bot.reply_to(message, "seleziona la foto: ")
    logger.debug("risposta inviata")
    bot.register_next_step_handler(message=message, callback=upload_foto_resize, prev_msg=[altezza, larghezza])


if __name__ == "__main__":
    create_save_location(SAVE_PATH)
    clean_up(SAVE_PATH)
    setuplog(LOG_PATH)
    bot.infinity_polling()

