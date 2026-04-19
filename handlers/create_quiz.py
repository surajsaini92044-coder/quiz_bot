from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states import QuizCreation
from keyboards import finish_quiz_kb, get_main_menu
import json
import os

router = Router()
QUIZZES_FILE = "quizzes.json"

if not os.path.exists(QUIZZES_FILE):
    with open(QUIZZES_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)

def load_quizzes():
    with open(QUIZZES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_quizzes(data):
    with open(QUIZZES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@router.callback_query(F.data == "create_quiz")
async def start_create_quiz(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("📝 Quiz ka **Title** bhejo:")
    await state.set_state(QuizCreation.waiting_title)
    await call.answer()

@router.message(QuizCreation.waiting_title)
async def process_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("📝 Quiz ka **Description** (optional - skip karne ke liye /skip):")
    await state.set_state(QuizCreation.waiting_description)

@router.message(QuizCreation.waiting_description)
async def process_description(message: Message, state: FSMContext):
    if message.text == "/skip":
        desc = ""
    else:
        desc = message.text
    await state.update_data(description=desc, questions=[])
    await message.answer(
        "✅ Quiz base ready!\n\n"
        "Ab pehla question bhejo (text only for now):",
        reply_markup=finish_quiz_kb()
    )
    await state.set_state(QuizCreation.waiting_question_text)

@router.message(QuizCreation.waiting_question_text)
async def process_question_text(message: Message, state: FSMContext):
    data = await state.get_data()
    questions = data.get("questions", [])
    questions.append({"text": message.text, "options": [], "correct": None, "time": 30, "shuffle": True})
    await state.update_data(questions=questions)
    await message.answer("🔢 Is question ke **options** bhejo (comma se separate, max 10)\nExample: A) Option1, B) Option2, C) Option3")
    await state.set_state(QuizCreation.waiting_options)

@router.message(QuizCreation.waiting_options)
async def process_options(message: Message, state: FSMContext):
    options = [opt.strip() for opt in message.text.split(",") if opt.strip()]
    if len(options) < 2 or len(options) > 10:
        await message.answer("❌ 2 se 10 options chahiye!")
        return
    data = await state.get_data()
    questions = data["questions"]
    questions[-1]["options"] = options
    await state.update_data(questions=questions)
    await message.answer(f"✅ Options saved!\nAb sahi jawab ka number bhejo (1 se {len(options)})")
    await state.set_state(QuizCreation.waiting_correct_option)

@router.message(QuizCreation.waiting_correct_option)
async def process_correct(message: Message, state: FSMContext):
    try:
        correct = int(message.text) - 1
        data = await state.get_data()
        questions = data["questions"]
        if correct < 0 or correct >= len(questions[-1]["options"]):
            raise ValueError
        questions[-1]["correct"] = correct
        await state.update_data(questions=questions)
        await message.answer("⏱ Time limit (seconds) bhejo (default 30):")
        await state.set_state(QuizCreation.waiting_time_limit)
    except:
        await message.answer("❌ Valid number bhejo!")

@router.message(QuizCreation.waiting_time_limit)
async def process_time(message: Message, state: FSMContext):
    try:
        time_limit = int(message.text) if message.text.isdigit() else 30
        data = await state.get_data()
        questions = data["questions"]
        questions[-1]["time"] = time_limit
        await state.update_data(questions=questions)
        await message.answer("🔀 Options shuffle karna hai? (yes/no)")
        await state.set_state(QuizCreation.waiting_shuffle)
    except:
        await message.answer("❌ Number bhejo!")

@router.message(QuizCreation.waiting_shuffle)
async def process_shuffle(message: Message, state: FSMContext):
    shuffle = message.text.lower() in ["yes", "ha", "1"]
    data = await state.get_data()
    questions = data["questions"]
    questions[-1]["shuffle"] = shuffle
    await state.update_data(questions=questions)
    await message.answer("✅ Question saved!\nAb choose karo:", reply_markup=finish_quiz_kb())

@router.callback_query(F.data == "add_question")
async def add_another_question(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("📝 Agla question text bhejo:")
    await state.set_state(QuizCreation.waiting_question_text)
    await call.answer()

@router.callback_query(F.data == "finish_quiz")
async def finish_quiz_creation(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    quizzes = load_quizzes()
    quiz_id = str(len(quizzes) + 1)
    quizzes[quiz_id] = {
        "user_id": call.from_user.id,
        "title": data["title"],
        "description": data.get("description", ""),
        "questions": data["questions"]
    }
    save_quizzes(quizzes)
    await call.message.edit_text(
        f"🎉 Quiz ban gaya!\nID: <code>{quiz_id}</code>\nTitle: {data['title']}\n"
        "Ab ise share karne ke liye dusre users ko ID batao ya /take_quiz use karo.",
        parse_mode="HTML"
    )
    await state.clear()
    await call.answer()
