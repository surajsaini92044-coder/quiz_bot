from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
import json
import os

router = Router()
QUIZZES_FILE = "quizzes.json"

def load_quizzes():
    if not os.path.exists(QUIZZES_FILE):
        return {}
    with open(QUIZZES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

@router.callback_query(F.data == "my_quizzes")
async def show_my_quizzes(call: CallbackQuery):
    quizzes = load_quizzes()
    user_id = str(call.from_user.id)
    
    user_quizzes = {qid: q for qid, q in quizzes.items() if str(q.get("user_id")) == user_id}
    
    if not user_quizzes:
        await call.message.edit_text(
            "❌ Aapne abhi tak koi quiz nahi banaya hai.\n"
            "Pehla quiz banane ke liye '📝 Quiz Banaye' button dabao.",
            reply_markup=None
        )
        await call.answer()
        return
    
    text = "📋 **Aapke Banaye Hue Quizzes**\n\n"
    for qid, q in user_quizzes.items():
        total_questions = len(q.get("questions", []))
        text += f"🆔 **ID:** `{qid}`\n"
        text += f"📌 **Title:** {q.get('title', 'No Title')}\n"
        text += f"❓ Questions: {total_questions}\n\n"
    
    text += "Kisi quiz ko share karne ke liye uska ID dusre users ko batao."
    
    await call.message.edit_text(text, parse_mode="Markdown")
    await call.answer()
