import os
from dotenv import load_dotenv
from server_utils import predict_server, grayscale_server, resize_server
from telebot.types import Message
from constants.paths import SAVE_PATH, LOG_PATH
from io_utils import create_save_location, save_image, clean_up
import telebot
from logger_utils import setuplog
import logging
from commands import START, PREDICTION, COMMANDS_LIST, HELP, GRAYSCALE, RESIZE

load_dotenv()

logger = logging.getLogger('my_logger')

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)


def show_menu(chat_id):
    elenco = "\n/".join(COMMANDS_LIST)
    bot.send_message(chat_id, f"Elenco comandi: \n/{elenco}")


def upload_foto_grayscale(message: Message) -> None:

    if message.photo is None:
        bot.reply_to(message, "il messaggio inviato non e' una foto")
        return None

    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    img_path = file_info.file_path

    downloaded_file = bot.download_file(img_path)
    save_image_path = SAVE_PATH + img_path[7:]
    save_image(downloaded_file, save_image_path)

    bot.reply_to(message, "immagine caricata con successo")
    logger.info(f"immagine salvata in: {save_image_path}")

    img_grayscale = grayscale_server(img_path[6:])
    save_image(img_grayscale, save_image_path)
    img_grayscale_path = save_image_path
    if img_grayscale is not None:
        with open(img_grayscale_path, "rb") as img:
            bot.send_photo(message.chat.id, img)
    else:
        logger.error("errore richiesta del server")
        bot.reply_to(message, "errore server")


def upload_foto_resize(message: Message, prev_msg) -> None:
    if message.photo is None:
        bot.reply_to(message, "il messaggio inviato non e' una foto")
        return None
    altezza = prev_msg[0]
    larghezza = prev_msg[1]
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    img_path = file_info.file_path

    downloaded_file = bot.download_file(img_path)
    save_image_path = SAVE_PATH + img_path[7:]
    save_image(downloaded_file, save_image_path)

    bot.reply_to(message, "immagine caricata con successo")
    logger.info(f"immagine salvata in: {save_image_path}")

    img_resize = resize_server(img_path[6:], altezza, larghezza)
    save_image(img_resize, save_image_path)
    img_grayscale_path = save_image_path
    if img_resize is not None:
        with open(img_grayscale_path, "rb") as img:
            bot.send_photo(message.chat.id, img)
    else:
        logger.error("errore richiesta del server")
        bot.reply_to(message, "errore server")


def upload_foto_predict(message: Message) -> None:

    if message.photo is None:
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

