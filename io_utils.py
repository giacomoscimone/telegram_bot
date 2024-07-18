import logging
import os

logger = logging.getLogger('my_logger')


def save_image(img: bytes, path: str) -> None:
    with open(path, 'wb') as file:
        file.write(img)
        logger.info("immagine salvata")


def create_save_location(save_location: str) -> None:
    os.makedirs(save_location, exist_ok=True)
    logger.debug("cartella immagini creata")


def clean_up(location_path: str) -> None:
    file_list = os.listdir(location_path)
    for file_path in file_list:
        os.remove(location_path + file_path)
        logger.debug(f"removed file: {location_path + file_path}")


def read_file(file_path: str) -> bytes:
    with open(file_path, 'rb') as file:
        return file.read()
