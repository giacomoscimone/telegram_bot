import requests
from constants.paths import SAVE_PATH
import logging
from constants.server import HOST_PATH, PORTA_SERVER, PREDICT_FUNCTION, GRAYSCALE_FUNCTION, RESIZE_FUNCTION
from io_utils import read_file

logger = logging.getLogger('my_logger')


def predict_server(file_path: str) -> (str, float):

    file = read_file(SAVE_PATH + file_path)

    files = [
        ('file', (file_path, file, 'image/jpeg'))
    ]
    logger.debug("immagine caricata dal predict")
    response = requests.post(f"{HOST_PATH}:{PORTA_SERVER}/{PREDICT_FUNCTION}/", files=files)
    logger.debug("immagine inviata al server")

    if response.status_code == 200:
        logger.info('Dati inviati con successo')

        message_dict = response.json()
        message = message_dict["message"]

        classe = message["class"]
        confidence = message["confidence"]

        return classe, confidence
    else:
        print('Errore nella richiesta')
        return None


def grayscale_server(file_path: str) -> (str, float):

    file = read_file(SAVE_PATH + file_path)

    files = [
        ('file', (file_path, file, 'image/jpeg'))
    ]
    logger.debug("immagine caricata dal predict")

    response = requests.post(f"{HOST_PATH}:{PORTA_SERVER}/{GRAYSCALE_FUNCTION}/", files=files)
    logger.debug("immagine inviata al server")

    if response.status_code == 200:
        logger.info('Dati inviati con successo')
        return response.content
    else:
        print('Errore nella richiesta')
        return None


def resize_server(file_path: str, altezza: int, larghezza: int) -> (str, float):

    file = read_file(SAVE_PATH + file_path)

    payload = {'altezza': altezza, 'larghezza': larghezza}

    files = [
        ('file', (file_path, file, 'image/jpeg'))
    ]
    logger.debug("immagine caricata dal predict")

    response = requests.post(f"{HOST_PATH}:{PORTA_SERVER}/{RESIZE_FUNCTION}/", data = payload, files=files)
    logger.debug("immagine inviata al server")

    if response.status_code == 200:
        logger.info('Dati inviati con successo')
        return response.content
    else:
        print('Errore nella richiesta')
        return None
