from telegram import ReplyKeyboardMarkup

def get_speakers_keyboard(speakers):
    return ReplyKeyboardMarkup(
        [[speaker["name"]] for speaker in speakers] + [["⬅️ Назад"]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
