from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
import json

router = Router()
QUIZZES_FILE = "quizzes.json"

def load_quizzes():
    with open(QUIZZES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

@router.callback_query(F.data == "take_quiz")
async def show_quizzes(call: CallbackQuery):
    quizzes = load_quizzes()
    if not quizzes:
        await call.message.edit_text("❌ Koi quiz nahi bana abhi!")
        return
    text = "Available Quizzes:\n\n"
    for qid, q in quizzes.items():
        text += f"ID: <code>{qid}</code> | {q['title']}\n"
    text += "\nQuiz ID bhejo (example: 1)"
    await call.message.edit_text(text, parse_mode="HTML")
    await call.answer()

@router.message()  # yahan quiz ID check karne ka simple logic (aap refine kar sakte ho)
async def handle_quiz_id(message: Message):
    quizzes = load_quizzes()
    if message.text in quizzes:
        quiz = quizzes[message.text]
        await message.answer(f"🎮 Starting Quiz: {quiz['title']}")
        # Yahan sequential poll bhej sakte ho (advanced logic aap add kar sakte ho)
        # Example: first question ka poll
        await message.answer("Quiz start! (full multi-question logic handlers mein add karo)")
    else:
        await message.answer("Invalid Quiz ID!")
