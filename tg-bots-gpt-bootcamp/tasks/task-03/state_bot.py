import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from dotenv import load_dotenv


class UserInfo(StatesGroup):
    name = State()
    favorite_language = State()
    experience = State()
    advice = State()

async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(UserInfo.name)
    await message.answer("Привет! Как тебя зовут?")


async def process_name(message: Message, state: FSMContext) -> None:
    data = await state.update_data(name=message.text)
    await state.set_state(UserInfo.favorite_language)

    name = data["name"]
    await message.answer(f"{name}, какой у тебя любимый язык программирования?")


async def process_language(message: Message, state: FSMContext) -> None:
    data = await state.update_data(favorite_language=message.text)
    match data["favorite_language"]:
        case "python":
            answer = "Понять и простить"
        case "c#":
            answer = "Это мой любимый язык тоже!"
        case "java":
            answer = "Рекомендую попробовать C# =)"
        case _:
            answer = "Не знаю такого языка =("

    name = (data["name"])
    #await state.clear()
    await message.answer(answer)
    await message.answer(f"{name}, сколько лет у тебя опыта разработки?")
    await state.set_state(UserInfo.experience)

async def process_experience(message, state):
    data = await state.update_data(experience=message.text)
    exp = data['experience']
    name = data['name']
    if exp < 1:
        await message.answer(f"{name}, you have {exp} (<1)")

    if exp >= 1 and exp <= 3:
        await message.answer(f"{name}, you have {exp} (1 <= exp <= 3)")

    if exp > 3 and exp < 10:
        await message.answer(f"{name}, you have {exp} (3 <= exp < 10)")

    if exp >= 10: 
        await message.answer(f"{name}, no advice required")
        await message.answer(f"{name}, give me advice")
        await state.set_state(UserInfo.experience)

async def main() -> None:
    # переименуй файл .env.dist в .env и подставь соотвествующие данные
    load_dotenv()
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

    dp = Dispatcher()
    dp.message.register(command_start, Command("start"))
    dp.message.register(process_name, UserInfo.name)
    dp.message.register(process_language, UserInfo.favorite_language)
    dp.message.register(process_experience, UserInfo.experience)

    bot = Bot(token=bot_token)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
