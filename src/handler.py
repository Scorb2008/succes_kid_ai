from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, BotCommand
from aiogram.enums import ChatAction
import asyncio

from src.neuro import NeuroAssistant
from src.keyboards import get_mode_keyboard
from .logger import setup_logger

logger = setup_logger()
router = Router()
assistant = NeuroAssistant()

db = []

async def set_bot_commands(bot):
    commands = [
        BotCommand(command="start", description="Начать работу с ботом"),
        BotCommand(command="child", description="Режим для детей"),
        BotCommand(command="parent", description="Режим для родителей"),
        BotCommand(command="help", description="Помощь и описание возможностей"),
    ]
    await bot.set_my_commands(commands)

@router.message(Command("start"))
async def start_cmd(message: Message):
    text = (
        "<b>🌸 Добро пожаловать в Успех AI 🌟</b>\n\n"
        "<i>Твой персональный помощник для детей и родителей❗️</i>\n\n"
        "Выбери режим:\n"
        "/child - для детей 👶\n"
        "/parent - для родителей 🧑‍🧑‍🧒\n\n"
        "Я стараюсь отвечать кратко и по делу! ✨"
    )
    await message.answer(text, reply_markup=get_mode_keyboard())


@router.message(Command("child"))
async def child_mode(message: Message):
    assistant.set_mode("child")
    await message.answer("🧒 Включил детский режим! Буду общаться как с другом-первоклассником!")


@router.message(Command("parent"))
async def parent_mode(message: Message):
    assistant.set_mode("parent")
    await message.answer("👨‍👩‍👧 Включил режим для родителей! Готов давать практические советы.")


@router.message(Command("help"))
async def help_cmd(message: Message):
    text = (
        "ℹ️ <b>Помощь</b>\n\n"
        "Я умею:\n"
        "• Общаться с детьми 6-8 лет\n"
        "• Помогать родителям с советами\n"
        "• Отвечать на вопросы просто и понятно\n\n"
        "Команды:\n"
        "/start - начать\n"
        "/child - детский режим\n"
        "/parent - режим для родителей\n"
        "/help - эта справка\n\n"
        "Просто напиши мне сообщение! 😊"
    )
    await message.answer(text)


@router.message(F.text)
async def handle_text(message: Message):
    if len(db) >= 15:
        await message.answer("Прости, я достиг предела сессии. Пожалуйста, начни новую с /start.")
        return
    else: 
        if len(message.text) > 500:
            await message.answer("Слишком длинное сообщение! Попробуй сказать короче. 😅")
            return

        user_text = message.text.strip()

        if not user_text:
            return

        await message.bot.send_chat_action(
            chat_id=message.chat.id,
            action=ChatAction.TYPING
        )

        try:
            await asyncio.sleep(0.5)

            response = await assistant.get_response(user_text)

            if len(response) > 4096:
                response = response[:4000] + "\n\n[сообщение было сокращено]"

            await message.answer(response)

        except Exception as e:
            print(f"Ошибка в обработке сообщения: {e}")
            await message.answer("Упс! Что-то пошло не так. Попробуй ещё раз! 🤔")



@router.callback_query(F.data.startswith("mode_"))
async def handle_mode_callback(callback: CallbackQuery):
    mode = callback.data.split("_")[1]

    if mode == "child":
        assistant.set_mode("child")
        await callback.message.answer("🧒 Включил детский режим! Теперь я твой весёлый друг!")
    elif mode == "parent":
        assistant.set_mode("parent")
        await callback.message.answer("👨‍👩‍👧 Включил режим для родителей! Задавайте вопросы!")

    await callback.answer(f"Режим изменён на {mode}")