import os


def save_image(img, path):
    with open(path, 'wb') as file:
        file.write(img)


def create_save_location(save_location: str) -> None:
    os.makedirs(save_location, exist_ok=True)
