import os
import time
from base64 import b64decode
from datetime import datetime
from io import BytesIO
import requests
from dotenv import load_dotenv
from PIL import Image



# переименуй файл .env.dist в .env и подставь соотвествующие данные
load_dotenv()
folder_id = os.getenv("YANDEX_FOLDER_ID")
api_key = os.getenv("YANDEX_API_KEY")
gpt_model = 'yandexgpt-lite'

def get_response_from_ai(data):
    print(data)
    user_prompt = f"{data['article_text']}{data['summary_length']}"

    system_prompt = 'Я тебе отправлю статью. Яз этой статьи я бы хотел видеть выжимку того, что там было написано. Я тебе дам указания, насколько длинным должен быть текст, а ты должен отправть мне только текст.'
    

    body = {
        'modelUri': f'gpt://{folder_id}/{gpt_model}',
        'completionOptions': {'stream': False, 'temperature': 0.3, 'maxTokens': 2000},
        'messages': [
            {'role': 'system', 'text': system_prompt},
            {'role': 'user', 'text': user_prompt},
        ],
    }
    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completionAsync'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Api-Key {api_key}'
    }

    response = requests.post(url, headers=headers, json=body)
    operation_id = response.json().get('id')

    url = f"https://llm.api.cloud.yandex.net:443/operations/{operation_id}"
    headers = {"Authorization": f"Api-Key {api_key}"}

    while True:
        response = requests.get(url, headers=headers)
        done = response.json()["done"]
        if done:
            break
        time.sleep(2)

    data = response.json()
    answer = data['response']['alternatives'][0]['message']['text']

    return answer


def get_image_from_ai(data):
    seed = int(round(datetime.now().timestamp()))

    prompt = data['img'] + data['style'] + data['colour']

    #prompt = "Милый пушистый котенок спит на спине. Octane render,f/2.8, ISO 200"

    body = {
        "modelUri": f"art://{folder_id}/yandex-art/latest",
        "generationOptions": {"seed": seed, "temperature": 0.6},
        "messages": [
            {"weight": 1, "text": prompt},
        ],
    }
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/imageGenerationAsync"
    headers = {"Authorization": f"Api-Key {api_key}"}

    response = requests.post(url, headers=headers, json=body)
    operation_id = response.json()["id"]

    url = f"https://llm.api.cloud.yandex.net:443/operations/{operation_id}"
    headers = {"Authorization": f"Api-Key {api_key}"}

    while True:
        response = requests.get(url, headers=headers)
        done = response.json()["done"]
        if done:
            break
        time.sleep(2)

    image_data = response.json()["response"]["image"]
    image_bytes = b64decode(image_data)
    image = Image.open(BytesIO(image_bytes))
    image.save("photo.png")

    return 1
