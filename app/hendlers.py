import asyncio
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import message, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from app.generate_photo import generate_image_from_text
import app.aio_keybord as kb
from app.key import email

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
    True_Or_False = State()

class oformlenie(StatesGroup):
    oform = State()
    t_or_f = State()


@router.message(CommandStart())
async def cmd_start(message: message, state: FSMContext):
    if app.baza.proverka(message.chat.id) == 1:
        await message.answer('Здравствуйте!', reply_markup=kb.main)
    else:
        await state.set_state(oformlenie.oform)
        await message.answer('Здравствуйте! Вам нужно оформить подписку.', reply_markup=kb.podpiska)

@router.message(oformlenie.oform)
async def oform(message: message, state: FSMContext):
    await state.update_data(style=message.text)
    await state.set_state(oformlenie.t_or_f)
    await message.answer('выберите верхную одежду', reply_markup=kb.outerwear)




@router.message(F.text == "Вернутся в главное меню")
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
async def shoes_Color(message: message, state: FSMContext, bot: Bot):
    await state.update_data(shoes_Color=message.text)
    data = await state.get_data()
    await message.answer('Подождите идёт генерация.')
    generate_image_from_text(f'изобрази человека на белом фоне {data["gender"]} пола, в {data["style"]} стиле. в {data["outerwear"]} {data["outerwear_Color"]} цвете, в {data["underwear"]} {data["underwear_Color"]} цвете, в {data["shoes"]} {data["shoes_Color"]} цвете')
    photo = FSInputFile(path='/home/trolololo22/PycharmProjects/telebotodejda/generated_image.jpg')
    await bot.send_photo(message.chat.id, photo=photo, reply_markup=kb.gotovo)
    await state.set_state(Generate.True_Or_False)


@router.message(Generate.True_Or_False)
async def trueOrFalse(message: message, state: FSMContext, bot: Bot):
    if message.text == "Перегенерировать":
        data = await state.get_data()
        await message.answer('Подождите идёт генерация.')
        generate_image_from_text(
            f'изобрази человека {data["gender"]} пола, в {data["style"]} стиле. в {data["outerwear"]} {data["outerwear_Color"]} цвете, в {data["underwear"]} {data["underwear_Color"]} цвете, в {data["shoes"]} {data["shoes_Color"]} цвете')
        photo = FSInputFile(path='/home/trolololo22/PycharmProjects/telebotodejda/generated_image.jpg')
        await bot.send_photo(message.chat.id, photo=photo, reply_markup=kb.gotovo)
    elif message.text == "задать вид заново":
        await state.set_state(Generate.gender)
        await message.answer('выберите пол', reply_markup=kb.gender)
    elif message.text == "Вернутся в главное меню":
        await state.clear()

@router.message(F.text == "Tex.поддежка")
async def teh_pomosh(message: message):
    await message.answer(f'Если у вас произошла произошла проблема то пишите сюда: {email}')

@router.message(F.text == "Tex.поддежка")
async def teh_pomosh(message: message):
    await message.answer(f'Если у вас произошла произошла проблема то пишите сюда: {email}')

@router.message(F.text == "проверить подписку")
async def teh_pomosh(message: message):
    await message.answer(app.baza.check(message.id))