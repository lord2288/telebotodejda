import asyncio
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import base64
import json
import requests
import time

import app.aio_keybord as kb

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

router = Router()

class Generate(StatesGroup):
    gender = State()
    style = State()

    outerwear = State()
    outerwear_Color = State()

    underwear = State()
    underwear_Color = State()

    shoes = State()
    shoes_Color = State()

@router.message(CommandStart())
async def cmd_start(message: message):
    await message.answer('Здравствуйте!', reply_markup=kb.main)
@router.message(F.text == "начать генерацию")
async def nachalo(message: message, state: FSMContext):
    await state.set_state(Generate.gender)
    await message.answer('выберите пол', reply_markup=kb.gender)
@router.message(Generate.gender)
async def Gen_gender(message: message, state: FSMContext):
    await state.update_data(gender=message.text)
    await state.set_state(Generate.style)
    await message.answer('выберите стиль', reply_markup=kb.style)

@router.message(Generate.style)
async def Gen_gender(message: message, state: FSMContext):
    await state.update_data(style=message.text)
    await state.set_state(Generate.outerwear)
    await message.answer('выберите верхную одежду', reply_markup=kb.outerwear)

@router.message(Generate.outerwear)
async def Gen_gender(message: message, state: FSMContext):
    await state.update_data(outerwear=message.text)
    await state.set_state(Generate.outerwear_Color)
    await message.answer('выберите цвет одежды')





@router.message(Generate.outerwear_Color)
async def Gen_gender(message: message, state: FSMContext):
    await state.update_data(outerwear_Color=message.text)
    await state.set_state(Generate.underwear)
    await message.answer('выберите верхную одежду', reply_markup=kb.underwear)

@router.message(Generate.underwear)
async def Gen_gender(message: message, state: FSMContext):
    await state.update_data(underwear=message.text)
    await state.set_state(Generate.underwear_Color)
    await message.answer('выберите цвет одежды')


@router.message(Generate.underwear_Color)
async def Gen_gender(message: message, state: FSMContext):
    await state.update_data(underwear_Color=message.text)
    await state.set_state(Generate.shoes)
    await message.answer('выберите верхную одежду', reply_markup=kb.shoes)


@router.message(Generate.shoes)
async def Gen_gender(message: message, state: FSMContext):
    await state.update_data(shoes=message.text)
    await state.set_state(Generate.shoes_Color)
    await message.answer('выберите цвет одежды')

@router.message(Generate.shoes_Color)
async def shoes_Color(message: message, state: FSMContext):
    await state.update_data(shoes_Color=message.text)
    data = await state.get_data()
    generate_image_from_text(f'изобрази человека {data["gender"]} пола, в {data["style"]} стиле. в {data["outerwear"]} {data["outerwear_Color"]} цвете, в {data["underwear"]} {data["underwear_Color"]} цвете, в {data["shoes"]} {data["shoes_Color"]} цвете')
    await message.answer_photo(photo='generated_image.jpg', reply_markup=kb.gotovo)

@router.message(F.text == "Перегенерировать" or F.text == 'задать вид заново')
async def trueOrFalse(message: message, state: FSMContext):
    if message.text == "Перегенерировать":
        data = await state.get_data()
        generate_image_from_text(
            f'изобрази человека {data["gender"]} пола, в {data["style"]} стиле. в {data["outerwear"]} {data["outerwear_Color"]} цвете, в {data["underwear"]} {data["underwear_Color"]} цвете, в {data["shoes"]} {data["shoes_Color"]} цвете')
        await message.answer_photo(photo='generated_image.jpg', reply_markup=kb.gotovo)
    elif message.text == "задать вид заново":
        await message.answer('выберите пол', reply_markup=kb.gender)


# async def send_photo(message: types.Message):
#    photo_path = os.path.join(os.getcwd(), 'photo_name.jpg')  # путь к вашей картинке
#    with open(photo_path, 'rb') as photo:
#       await bot.send_photo(message.chat.id, photo)

 # gender = State()
 #    style = State()
 #
 #    outerwear = State()
 #    outerwear_Color = State()
 #
 #    underwear = State()
 #    underwear_Color = State()
 #
 #    shoes = State()
 #    shoes_Color = State()