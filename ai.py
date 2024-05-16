import os
import base64
import requests
import json
import time

# Функция для обращения к API и генерации изображения на основе текста
def generate_image_from_text(prompt):
    url = 'https://api-key.fusionbrain.ai/'
    api_key = 'C620606DC592BF60C4462E27F5309E12'
    secret_key = '40D31C36DFDBD37DD3C385A7B5C143B4'
    auth_headers = {
        'X-Key': f'Key {api_key}',
        'X-Secret': f'Secret {secret_key}',
    }

    # Получаем ID модели
    response = requests.get(f"{url}key/api/v1/models", headers=auth_headers)
    response.raise_for_status()
    model_id = response.json()[0]['id']

    # Запрос на генерацию изображения
    params = {
        "type": "GENERATE",
        "numImages": 1,
        "width": 1024,
        "height": 1024,
        "generateParams": {"query": prompt}
    }
    data = {
        'model_id': (None, model_id),
        'params': (None, json.dumps(params), 'application/json')
    }
    response = requests.post(f"{url}key/api/v1/text2image/run", headers=auth_headers, files=data)
    response.raise_for_status()
    uuid = response.json()['uuid']

    # Проверка статуса генерации
    for _ in range(10):
        response = requests.get(f"{url}key/api/v1/text2image/status/{uuid}", headers=auth_headers)
        response.raise_for_status()
        data = response.json()
        if data['status'] == 'DONE':
            images = data['images']
            image_data = base64.b64decode(images[0])
            filename = f"generated_image.jpg"
            try:
                with open(filename, "wb") as file:
                    file.write(image_data)
                print(f"Изображение успешно сохранено как {filename}")
                return
            except Exception as e:
                print(f"Не удалось сохранить изображение: {e}")
                return
        time.sleep(10)
    print("Не удалось сгенерировать изображение.")


if __name__ == "__main__":
    # Ввод текста для генерации изображения
    prompt = input("Введите запрос: ").strip()
    generate_image_from_text(prompt)
