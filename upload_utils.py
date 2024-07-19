import os
import telebot
import logging
import cv2

from dotenv import load_dotenv
from telebot.types import Message
from constants.paths import SAVE_PATH
from io_utils import save_image
from server_utils import predict_server, grayscale_server, resize_server

load_dotenv()

logger = logging.getLogger('my_logger')

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)


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

    img = cv2.imread(save_image_path)

    alt_img = img.shape[0]
    larg_img = img.shape[1]

    if altezza < 0 or larghezza < 0 or altezza > alt_img or larghezza > larg_img:
        bot.reply_to(message, "i valori inseriti di altezza o larghezza non sono accettabili")
        return None

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
