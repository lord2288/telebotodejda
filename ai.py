import os
import base64
from random import randint as r
import requests
import json
import time


class Text2ImageAPI:
    def init(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        if response.status_code == 401:
            raise ValueError("Unauthorized: Check your API key and secret key.")
        response.raise_for_status()
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }

        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        if response.status_code == 401:
            raise ValueError("Unauthorized: Check your API key and secret key.")
        response.raise_for_status()
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            if response.status_code == 401:
                raise ValueError("Unauthorized: Check your API key and secret key.")
            response.raise_for_status()
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']
            attempts -= 1
            time.sleep(delay)
        return None


def gen(prom, dirr="res"):
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', 'C620606DC592BF60C4462E27F5309E12', '40D31C36DFDBD37DD3C385A7B5C143B4')
    model_id = api.get_model()
    uuid = api.generate(prom, model_id)
    images = api.check_generation(uuid)

    if not images:
        print("Failed to generate image.")
        return

    image_base64 = images[0]
    image_data = base64.b64decode(image_base64)

    os.makedirs(dirr, exist_ok=True)
    filename = f"{dirr}/{prom.replace(' ', '_')}_{r(0, 100000)}.jpg"

    try:
        with open(filename, "wb") as file:
            file.write(image_data)
        print(f"Image saved successfully as {filename}")
    except Exception as e:
        print(f"Failed to save the image: {e}")


while True:
    i = input("prompt: ")

    dir_name = i.replace("\n", " ").split(".")[0]
    dir_path = os.path.join(os.getcwd().replace("\\", "/"), dir_name)

    try:
        os.mkdir(dir_path)
    except FileExistsError:
        print('Directory already exists')

    for j in range(4):
        gen(i.replace("\n", " "), dir_name)
        print(f"Image {j + 1} generated")

    print("Generation completed")