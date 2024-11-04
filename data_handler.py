import json
import os

DATA_FILE = "gif_data.json"

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            try:
                data = json.load(file)
                if isinstance(data, list):
                    return data
                else:
                    print("Advertencia: El archivo de datos no contiene una lista. Reiniciando datos.")
                    return []
            except json.JSONDecodeError:
                print("Advertencia: Error de decodificación en el archivo de datos. Reiniciando datos.")
                return []
    return []
