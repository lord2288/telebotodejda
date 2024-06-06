import base64
import json
import requests
import time

def generate_image_from_text(prompt):
    try:
        url = 'https://api-key.fusionbrain.ai/'
        api_key = 'C620606DC592BF60C4462E27F5309E12'
        secret_key = '40D31C36DFDBD37DD3C385A7B5C143B4'
        headers = {'X-Key': f'Key {api_key}', 'X-Secret': f'Secret {secret_key}'}
        response = requests.get(f"{url}key/api/v1/models", headers=headers)
        response.raise_for_status()
        model_id = response.json()[0]['id']
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
        response = requests.post(f"{url}key/api/v1/text2image/run", headers=headers, files=data)
        response.raise_for_status()
        uuid = response.json()['uuid']
        for _ in range(10):
            response = requests.get(f"{url}key/api/v1/text2image/status/{uuid}", headers=headers)
            response.raise_for_status()
            data = response.json()
            if data['status'] == 'DONE':
                image_data = base64.b64decode(data['images'][0])
                filename = "generated_image.jpg"
                with open(filename, "wb") as file:
                    file.write(image_data)
                return filename
            time.sleep(10)
        return None
    except Exception as e:
        print(f"Error generating image: {e}")
        return None