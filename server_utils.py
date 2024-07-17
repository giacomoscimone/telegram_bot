import requests
from costant_path import SAVE_PATH


def predict_server(file_path):

    files = [
        ('file', (file_path, open(SAVE_PATH + file_path, 'rb'), 'image/jpeg'))
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
