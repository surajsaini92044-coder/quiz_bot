import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

# Config
from config import BOT_TOKEN

# Handlers
from handlers.commands import router as commands_router
from handlers.create_quiz import router as create_router
from handlers.take_quiz import router as take_router
from handlers.my_quizzes import router as my_quizzes_router
from handlers.leaderboard import router as leaderboard_router


async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())

    # Sab routers add kar rahe hain
    dp.include_router(commands_router)
    dp.include_router(create_router)
    dp.include_router(take_router)
    dp.include_router(my_quizzes_router)
    dp.include_router(leaderboard_router)

    print("🚀 QuizBot successfully started... @YourQuizBot")
    print("Bot is now polling...")

    # Bot start
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
