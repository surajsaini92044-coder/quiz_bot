from aiogram import Router, F
from aiogram.types import CallbackQuery
import json
import os

router = Router()
QUIZZES_FILE = "quizzes.json"
SCORES_FILE = "scores.json"   # scores store karne ke liye

def load_quizzes():
    if not os.path.exists(QUIZZES_FILE):
        return {}
    with open(QUIZZES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def load_scores():
    if not os.path.exists(SCORES_FILE):
        return {}
    with open(SCORES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_scores(scores):
    with open(SCORES_FILE, "w", encoding="utf-8") as f:
        json.dump(scores, f, ensure_ascii=False, indent=2)

@router.callback_query(F.data == "leaderboard")
async def show_leaderboard(call: CallbackQuery):
    scores = load_scores()
    
    if not scores:
        await call.message.edit_text(
            "🏆 Abhi koi scores nahi hain.\n"
            "Pehla quiz khelo aur leaderboard populate karo!",
            reply_markup=None
        )
        await call.answer()
        return
    
    # Simple global top 10 by score
    sorted_scores = sorted(scores.items(), key=lambda x: x[1].get("score", 0), reverse=True)[:10]
    
    text = "🏆 **Global Leaderboard**\n\n"
    for i, (user_id, data) in enumerate(sorted_scores, 1):
        username = data.get("username", f"User {user_id}")
        score = data.get("score", 0)
        total = data.get("total_questions", 1)
        accuracy = round((score / total) * 100) if total > 0 else 0
        
        text += f"{i}. 👤 **{username}**\n"
        text += f"   Score: {score}/{total} ({accuracy}%)\n\n"
    
    text += "Note: Yeh basic leaderboard hai. Baad mein har quiz ka alag leaderboard add kar sakte hain."
    
    await call.message.edit_text(text, parse_mode="Markdown")
    await call.answer()
