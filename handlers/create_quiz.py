from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states import QuizCreation
from keyboards import finish_quiz_kb, get_main_menu
import json
import os

router = Router()
QUIZZES_FILE = "quizzes.json"

def load_quizzes():
    if not os.path.exists(QUIZZES_FILE):
        return {}
    try:
        with open(QUIZZES_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            return json.loads(content) if content else {}
    except:
        return {}

def save_quizzes(data):
    with open(QUIZZES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ====================== CREATE QUIZ FLOW ======================

@router.callback_query(F.data == "create_quiz")
async def start_create_quiz(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        "Let's create a new quiz.\n\n"
        "Pehle quiz ka **Title** bhejo (jaise: 'Aptitude Test' ya 'GK Quiz')",
        parse_mode="Markdown"
    )
    await state.set_state(QuizCreation.waiting_title)
    await call.answer()

@router.message(QuizCreation.waiting_title)
async def process_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text, questions=[])
    await message.answer(
        "Good. Ab quiz ka **Description** bhejo (optional).\n"
        "Skip karne ke liye /skip likho."
    )
    await state.set_state(QuizCreation.waiting_description)

@router.message(QuizCreation.waiting_description)
async def process_description(message: Message, state: FSMContext):
    desc = "" if message.text == "/skip" else message.text
    await state.update_data(description=desc)
    
    await message.answer(
        "✅ Good!\n\n"
        "Ab **pehla question** create karo.\n\n"
        "→ Question text bhejo\n"
        "→ Photo/Video/GIF bhej sakte ho (optional)\n"
        "→ Phir options ke saath poll bhej sakte ho.",
        reply_markup=finish_quiz_kb()
    )
    await state.set_state(QuizCreation.waiting_question_text)

@router.message(QuizCreation.waiting_question_text)
async def process_question(message: Message, state: FSMContext):
    data = await state.get_data()
    questions = data.get("questions", [])
    
    # Media check (photo, video, document, animation)
    media_file_id = None
    media_type = None
    
    if message.photo:
        media_file_id = message.photo[-1].file_id
        media_type = "photo"
    elif message.video:
        media_file_id = message.video.file_id
        media_type = "video"
    elif message.animation:
        media_file_id = message.animation.file_id
        media_type = "animation"

    questions.append({
        "text": message.text or "Question",
        "media_file_id": media_file_id,
        "media_type": media_type,
        "options": [],
        "correct": None,
        "time": 30
    })

    await state.update_data(questions=questions)
    
    await message.answer(
        "Question saved!\n\n"
        "Ab is question ke **options** bhejo comma se alag karke:\n"
        "Example: Delhi, Mumbai, Kolkata, Chennai"
    )
    await state.set_state(QuizCreation.waiting_options)

# Baaki functions (options, correct answer, time, finish) same rakh sakte ho
# Ya purana code yahan se jod lo

@router.callback_query(F.data == "finish_quiz")
async def finish_quiz_creation(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    quizzes = load_quizzes()
    quiz_id = str(len(quizzes) + 1)
    
    quizzes[quiz_id] = {
        "user_id": call.from_user.id,
        "title": data.get("title", "Untitled Quiz"),
        "description": data.get("description", ""),
        "questions": data.get("questions", [])
    }
    
    save_quizzes(quizzes)
    
    await call.message.edit_text(
        f"🎉 **Quiz Successfully Created!**\n\n"
        f"🆔 Quiz ID: `{quiz_id}`\n"
        f"📌 Title: {data.get('title')}\n"
        f"❓ Questions: {len(data.get('questions', []))}\n\n"
        f"Ab ise share karne ke liye Quiz ID dusron ko batao.",
        parse_mode="Markdown"
    )
    await state.clear()
