from telegram import ReplyKeyboardMarkup

def get_speaker_keyboard():
    return ReplyKeyboardMarkup(
        [["⬅️ Назад"]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
