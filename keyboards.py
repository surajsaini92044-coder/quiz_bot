from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Quiz Banaye", callback_data="create_quiz")],
        [InlineKeyboardButton(text="🎮 Quiz Khele", callback_data="take_quiz")],
        [InlineKeyboardButton(text="📋 Mera Quiz", callback_data="my_quizzes")],
        [InlineKeyboardButton(text="🏆 Leaderboard", callback_data="leaderboard")]
    ])

def finish_quiz_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Quiz Finish Karo", callback_data="finish_quiz")],
        [InlineKeyboardButton(text="➕ Aur Question Add Karo", callback_data="add_question")]
    ])
