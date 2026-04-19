from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from keyboards import get_main_menu

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 Welcome to **QuizBot**!\n\n"
        "Yahan aap apna quiz bana sakte ho aur dusron ko share kar sakte ho.\n"
        "Choose option below 👇",
        reply_markup=get_main_menu()
    )

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Commands:\n/start - Main menu\n/myquizzes - Apne quizzes\n/leaderboard - Top scorers")
