import os
from dotenv import load_dotenv
import requests
import telebot
from telebot.types import Message
import json

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

PATH = "C:\\Users\\Alternanza\\Documents\\GitHub\\telegram_bot\\"


def save_image(img, path):
    with open(path, 'wb') as file:
        file.write(img)


def upload_foto(message: Message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    save_image(downloaded_file, PATH + file_info.file_path[6:])
    bot.reply_to(message, "immagine caricata con successo")

    classe, confidence = upload_server(file_info.file_path[6:])
    if classe is not None:
        bot.reply_to(message, f"E' una {classe}!\n(Sono sicuro al {round(confidence*100)}%)")


def upload_server(file_path):

    files = [
        ('file', (file_path, open(PATH + file_path, 'rb'), 'image/jpeg'))
    ]
    response = requests.post('http://localhost:8000/upload-image/', files=files)

    if response.status_code == 200:
        print('Dati inviati con successo')

        convert_dizionario = response.json()
        message = convert_dizionario["message"]
        
        classe = message["class"]
        confidence = message["confidence"]

        return classe, confidence
    else:
        print('Errore nella richiesta')
        return None


@bot.message_handler(commands=['predizione'])
def class_prediction(message: Message):
    bot.reply_to(message, "seleziona la foto: ")
    bot.register_next_step_handler(message=message, callback=upload_foto)


bot.infinity_polling()
