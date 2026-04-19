from aiogram.fsm.state import StatesGroup, State

class QuizCreation(StatesGroup):
    waiting_title = State()
    waiting_description = State()
    waiting_question_text = State()
    waiting_options = State()
    waiting_correct_option = State()
    waiting_time_limit = State()
    waiting_shuffle = State()
