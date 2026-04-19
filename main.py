import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from aiogram.fsm.storage.memory import MemoryStorage
from handlers.commands import router as commands_router
from handlers.create_quiz import router as create_router
from handlers.take_quiz import router as take_router

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    
    dp.include_router(commands_router)
    dp.include_router(create_router)
    dp.include_router(take_router)
    
    print("🚀 QuizBot started...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
