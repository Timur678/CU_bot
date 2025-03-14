import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv


# Определяем состояния диалога
class BookData(StatesGroup):
    waiting_for_grade = State()
    waiting_for_subject = State()
    waiting_for_textbook = State()
    waiting_for_author = State()
    waiting_for_confirmation = State()


# Функции для формирования inline‑клавиатур
def get_grade_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="9 класс", callback_data="grade_9"),
         InlineKeyboardButton(text="10 класс", callback_data="grade_10")],
        [InlineKeyboardButton(text="11 класс", callback_data="grade_11")]
    ])


def get_subject_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Математика", callback_data="subject_math"),
         InlineKeyboardButton(text="Физика", callback_data="subject_physics"),
         InlineKeyboardButton(text="Информатика", callback_data="subject_informatics")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_grade")]
    ])


def get_textbook_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Учебник 1", callback_data="textbook_1"),
         InlineKeyboardButton(text="Учебник 2", callback_data="textbook_2")],
        [InlineKeyboardButton(text="Учебник 3", callback_data="textbook_3")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_subject")]
    ])


def get_author_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Автор A", callback_data="author_A"),
         InlineKeyboardButton(text="Автор B", callback_data="author_B")],
        [InlineKeyboardButton(text="Автор C", callback_data="author_C")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_textbook")]
    ])


def get_confirmation_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Подтвердить выбор", callback_data="confirm"),
         InlineKeyboardButton(text="Изменить выбор", callback_data="change")]
    ])


def get_edit_options_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Изменить класс", callback_data="edit_grade")],
        [InlineKeyboardButton(text="Изменить предмет", callback_data="edit_subject")],
        [InlineKeyboardButton(text="Изменить учебник", callback_data="edit_textbook")],
        [InlineKeyboardButton(text="Изменить автора", callback_data="edit_author")]
    ])


# Обработчик команды /start
async def command_start(message: Message, state: FSMContext):
    await state.clear()
    sent = await message.answer("Пожалуйста, выберите класс:", reply_markup=get_grade_keyboard())
    # Сохраняем id сообщения для дальнейшего удаления, если потребуется вернуться назад
    await state.update_data(grade_msg_id=sent.message_id)
    await state.set_state(BookData.waiting_for_grade)


# Обработчик выбора класса
async def grade_selected(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data  # например, "grade_9"
    # Используем маппинг, чтобы сохранить полное название папки
    grade_mapping = {"9": "9 класс", "10": "10 класс", "11": "11 класс"}
    grade_key = data.split("_")[1]
    grade = grade_mapping.get(grade_key, grade_key)
    await state.update_data(grade=grade, subject=None, textbook=None, author=None)
    await callback_query.message.edit_text(f"Вы выбрали {grade}")
    new_msg = await callback_query.bot.send_message(
        callback_query.message.chat.id,
        f"Выбран класс: {grade}. Пожалуйста, выберите предмет:",
        reply_markup=get_subject_keyboard()
    )
    await state.update_data(subject_msg_id=new_msg.message_id)
    await state.set_state(BookData.waiting_for_subject)
    await callback_query.answer()


# Обработчик выбора предмета
async def subject_selected(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data  # например, "subject_physics"
    subject_mapping = {"math": "Математика", "physics": "Физика", "informatics": "Информатика"}
    subject_key = data.split("_")[1]
    subject = subject_mapping.get(subject_key, subject_key)
    stored_data = await state.get_data()
    if stored_data.get("subject_edit_mode"):
        # Если выбран режим редактирования предмета, обновляем только предмет
        await state.update_data(subject=subject, subject_edit_mode=False)
        try:
            await callback_query.message.delete()
        except Exception:
            pass
        updated_data = await state.get_data()
        summary = (
            f"Ваш выбор:\n"
            f"Класс: {updated_data.get('grade')}\n"
            f"Предмет: {subject}\n"
            f"Учебник: {updated_data.get('textbook')}\n"
            f"Автор: {updated_data.get('author')}"
        )
        confirm_msg_id = updated_data.get("confirm_msg_id")
        if confirm_msg_id:
            try:
                await callback_query.bot.delete_message(callback_query.message.chat.id, confirm_msg_id)
            except Exception:
                pass
        new_msg = await callback_query.bot.send_message(
            callback_query.message.chat.id,
            summary,
            reply_markup=get_confirmation_keyboard()
        )
        await state.update_data(confirm_msg_id=new_msg.message_id)
        await state.set_state(BookData.waiting_for_confirmation)
    else:
        # Обычный сценарий: при выборе предмета сбрасываем учебник и автора
        await state.update_data(subject=subject, textbook=None, author=None)
        try:
            await callback_query.message.delete()
        except Exception:
            pass
        new_msg = await callback_query.bot.send_message(
            callback_query.message.chat.id,
            f"Выбран предмет: {subject}. Пожалуйста, выберите учебник:",
            reply_markup=get_textbook_keyboard()
        )
        await state.update_data(textbook_msg_id=new_msg.message_id)
        await state.set_state(BookData.waiting_for_textbook)
    await callback_query.answer()


# Обработчик выбора учебника
async def textbook_selected(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data  # например, "textbook_1"
    textbook_num = data.split("_")[1]
    textbook = f"Учебник {textbook_num}"
    await state.update_data(textbook=textbook, author=None)
    await callback_query.message.edit_text(f"Вы выбрали {textbook}")
    new_msg = await callback_query.bot.send_message(
        callback_query.message.chat.id,
        f"Выбран учебник: {textbook}. Пожалуйста, выберите автора:",
        reply_markup=get_author_keyboard()
    )
    await state.update_data(author_msg_id=new_msg.message_id)
    await state.set_state(BookData.waiting_for_author)
    await callback_query.answer()


# Обработчик выбора автора
async def author_selected(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data  # например, "author_A"
    author_mapping = {"A": "Автор A", "B": "Автор B", "C": "Автор C"}
    author_key = data.split("_")[1]
    author = author_mapping.get(author_key, author_key)
    await state.update_data(author=author)
    await callback_query.message.edit_text(f"Вы выбрали {author}")
    user_data = await state.get_data()
    summary = (
        f"Ваш выбор:\n"
        f"Класс: {user_data.get('grade')}\n"
        f"Предмет: {user_data.get('subject')}\n"
        f"Учебник: {user_data.get('textbook')}\n"
        f"Автор: {user_data.get('author')}"
    )
    new_msg = await callback_query.bot.send_message(
        callback_query.message.chat.id,
        summary,
        reply_markup=get_confirmation_keyboard()
    )
    await state.update_data(confirm_msg_id=new_msg.message_id)
    await state.set_state(BookData.waiting_for_confirmation)
    await callback_query.answer()


# При подтверждении выбора выводим данные в консоль, формируем путь к файлу и отправляем его пользователю
async def confirm_selection(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    print("User confirmed selection:", user_data)
    
    # Формируем путь к файлу по структуре:
    # <Grade>/<Author>/<Subject>/<Book>.txt
    grade = user_data.get("grade")       # например, "9 класс"
    author = user_data.get("author")     # например, "Автор A"
    subject = user_data.get("subject")   # например, "Физика"
    textbook = user_data.get("textbook") # например, "Учебник 1"
    base_dir = r"C:\Users\User\Desktop\Timur"  # базовая директория
    file_path = os.path.join(base_dir, grade, author, subject, textbook + ".pdf")
    
    chat_id = callback_query.message.chat.id
    await callback_query.bot.send_message(chat_id, "Выбор подтвержден")
    if os.path.exists(file_path):
        try:
            document = types.FSInputFile(file_path)
            await callback_query.bot.send_document(chat_id, document)
        except Exception as e:
            await callback_query.bot.send_message(chat_id, f"Ошибка при отправке книги: {e}")
    else:
        await callback_query.bot.send_message(chat_id, f"Книга не найдена по пути: {file_path}")
    
    await callback_query.message.delete()
    #await callback_query.bot.send_message(chat_id, "Выбор подтвержден")
    await state.clear()
    await callback_query.answer()


# --- Обработчики кнопок "Назад" и редактирования ---

async def back_to_grade(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    chat_id = callback_query.message.chat.id
    await callback_query.message.delete()
    grade_msg_id = data.get("grade_msg_id")
    if grade_msg_id:
        try:
            await callback_query.bot.delete_message(chat_id, grade_msg_id)
        except Exception:
            pass
    await state.update_data(grade=None, subject=None, textbook=None, author=None,
                              grade_msg_id=None, subject_msg_id=None, textbook_msg_id=None)
    new_msg = await callback_query.bot.send_message(chat_id, "Пожалуйста, выберите класс:", reply_markup=get_grade_keyboard())
    await state.update_data(grade_msg_id=new_msg.message_id)
    await state.set_state(BookData.waiting_for_grade)
    await callback_query.answer()


async def back_to_subject(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    chat_id = callback_query.message.chat.id
    await callback_query.message.delete()
    subject_msg_id = data.get("subject_msg_id")
    if subject_msg_id:
        try:
            await callback_query.bot.delete_message(chat_id, subject_msg_id)
        except Exception:
            pass
    grade = data.get("grade")
    await state.update_data(subject=None, textbook=None, author=None,
                              subject_msg_id=None, textbook_msg_id=None)
    new_msg = await callback_query.bot.send_message(chat_id,
        f"Выбран класс: {grade}. Пожалуйста, выберите предмет:",
        reply_markup=get_subject_keyboard())
    await state.update_data(subject_msg_id=new_msg.message_id)
    await state.set_state(BookData.waiting_for_subject)
    await callback_query.answer()


async def back_to_textbook(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    chat_id = callback_query.message.chat.id
    await callback_query.message.delete()
    textbook_msg_id = data.get("textbook_msg_id")
    if textbook_msg_id:
        try:
            await callback_query.bot.delete_message(chat_id, textbook_msg_id)
        except Exception:
            pass
    subject = data.get("subject")
    await state.update_data(textbook=None, author=None, textbook_msg_id=None)
    new_msg = await callback_query.bot.send_message(chat_id,
        f"Выбран предмет: {subject}. Пожалуйста, выберите учебник:",
        reply_markup=get_textbook_keyboard())
    await state.update_data(textbook_msg_id=new_msg.message_id)
    await state.set_state(BookData.waiting_for_textbook)
    await callback_query.answer()

async def change_selection(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await callback_query.bot.send_message(callback_query.message.chat.id,
        "Что бы вы хотели изменить?", reply_markup=get_edit_options_keyboard())
    await callback_query.answer()


async def edit_grade(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await state.clear()
    new_msg = await callback_query.bot.send_message(callback_query.message.chat.id,
        "Пожалуйста, выберите класс:", reply_markup=get_grade_keyboard())
    await state.update_data(grade_msg_id=new_msg.message_id)
    await state.set_state(BookData.waiting_for_grade)
    await callback_query.answer()


async def edit_subject(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    chat_id = callback_query.message.chat.id
    await callback_query.message.delete()
    # Очищаем только значение предмета и устанавливаем флаг редактирования
    await state.update_data(subject=None, subject_edit_mode=True, subject_msg_id=None)
    new_msg = await callback_query.bot.send_message(chat_id,
        f"Выбран класс: {data.get('grade')}. Пожалуйста, выберите новый предмет:",
        reply_markup=get_subject_keyboard())
    await state.update_data(subject_msg_id=new_msg.message_id)
    await state.set_state(BookData.waiting_for_subject)
    await callback_query.answer()


async def edit_textbook(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    chat_id = callback_query.message.chat.id
    await callback_query.message.delete()
    subject = data.get("subject")
    await state.update_data(textbook=None, author=None, textbook_msg_id=None)
    new_msg = await callback_query.bot.send_message(chat_id,
        f"Выбран предмет: {subject}. Пожалуйста, выберите учебник:",
        reply_markup=get_textbook_keyboard())
    await state.update_data(textbook_msg_id=new_msg.message_id)
    await state.set_state(BookData.waiting_for_textbook)
    await callback_query.answer()


async def edit_author(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    chat_id = callback_query.message.chat.id
    await callback_query.message.delete()
    textbook = data.get("textbook")
    await state.update_data(author=None)
    new_msg = await callback_query.bot.send_message(chat_id,
        f"Выбран учебник: {textbook}. Пожалуйста, выберите автора:",
        reply_markup=get_author_keyboard())
    await state.update_data(author_msg_id=new_msg.message_id)
    await state.set_state(BookData.waiting_for_author)
    await callback_query.answer()


async def main() -> None:
    load_dotenv()
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        raise Exception("TELEGRAM_BOT_TOKEN не найден в переменных окружения.")
    bot = Bot(token=bot_token)
    dp = Dispatcher()
    
    dp.message.register(command_start, Command("start"))
    dp.callback_query.register(grade_selected, lambda c: c.data and c.data.startswith("grade_"))
    dp.callback_query.register(subject_selected, lambda c: c.data and c.data.startswith("subject_"))
    dp.callback_query.register(textbook_selected, lambda c: c.data and c.data.startswith("textbook_"))
    dp.callback_query.register(author_selected, lambda c: c.data and c.data.startswith("author_"))
    
    dp.callback_query.register(back_to_grade, lambda c: c.data == "back_to_grade")
    dp.callback_query.register(back_to_subject, lambda c: c.data == "back_to_subject")
    dp.callback_query.register(back_to_textbook, lambda c: c.data == "back_to_textbook")
    
    dp.callback_query.register(confirm_selection, lambda c: c.data == "confirm")
    dp.callback_query.register(change_selection, lambda c: c.data == "change")
    dp.callback_query.register(edit_grade, lambda c: c.data == "edit_grade")
    dp.callback_query.register(edit_subject, lambda c: c.data == "edit_subject")
    dp.callback_query.register(edit_textbook, lambda c: c.data == "edit_textbook")
    dp.callback_query.register(edit_author, lambda c: c.data == "edit_author")
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())