import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, FSInputFile
from dotenv import load_dotenv
from ai_module_text import get_response_from_ai, get_image_from_ai
from PIL import Image


class TextSummary(StatesGroup):
    article_text = State()
    article_summary_length = State()

class ImageGenerate(StatesGroup):
    img = State()
    style = State()
    colour = State()


async def command_start(message):
    await message.answer("Этот бот может тебе либо сгенировать текст на основе статьи (/summary), либо сгенерировать картинку (/image)")


async def command_image(message, state):
    await state.set_state(ImageGenerate.img)
    await message.answer("Что бы ты хотел увидеть на картинке?")

async def process_image_generate(message, state):
    msg = message.text
    data = await state.update_data(img=msg)
    await state.set_state(ImageGenerate.style)
    await message.answer(f"Какой стиль? Реалистичный или нет?")

async def process_image_style(message, state):
    msg = (message.text).lower().strip()
    if msg not in ['реалистичный', 'не реалистичный']:
        await message.answer("Стили может быть только реалистиным или не реалистичным!!!")
        return 

    data = await state.update_data(style=msg)
    await state.set_state(ImageGenerate.colour)
    await message.answer(f"Какой цвет?")

async def process_image_colour(message, state):
    data = await state.update_data(colour=message.text)
    print(data)
    status = get_image_from_ai(data)
    if status:
        photo = FSInputFile("photo.png")
        await message.answer_photo(photo=photo)

async def command_summary(message: Message, state: FSMContext) -> None:
    await state.set_state(TextSummary.article_text)
    await message.answer("Привет! Отправь мне текст статьи")


async def process_article_text(message: Message, state: FSMContext) -> None:
    msg = message.text
    if len(msg) < 10:
        await message.answer("Статья очень маленькая!")
        return 
    
    data = await state.update_data(article_text=message.text)
    await state.set_state(TextSummary.article_summary_length)
    await message.answer(f"Ты хочешь подробно или нет? Напиши Да или Нет")


async def process_article_summary_length(message: Message, state: FSMContext) -> None:
    msg = (message.text).lower().strip()
    print(msg)
    if msg not in ['да', 'нет']:
        await message.answer(f"Только да или нет!!!")
        return 
    
    data = await state.update_data(article_summary_length=msg)
    
    ai_reponse = send_ai_generated_text(data)
    await message.answer(f"{ai_reponse}")


def send_ai_generated_text(data):
    msg = data['article_summary_length']
    
    if msg == "да":
        data['summary_length'] = 'Напиши подробно'
    else:
        data['summary_length'] = "Напиши коротко"

    response = get_response_from_ai(data)  
    return response
    


async def main() -> None:
    # переименуй файл .env.dist в .env и подставь соотвествующие данные
    load_dotenv()
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

    dp = Dispatcher()
    dp.message.register(command_start, Command("start"))
    dp.message.register(command_summary, Command("summary"))
    dp.message.register(command_image, Command("image"))
    dp.message.register(process_article_text, TextSummary.article_text)
    dp.message.register(process_article_summary_length, TextSummary.article_summary_length)
    dp.message.register(process_image_generate, ImageGenerate.img)
    dp.message.register(process_image_style, ImageGenerate.style)
    dp.message.register(process_image_colour, ImageGenerate.colour)


    bot = Bot(token=bot_token)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
