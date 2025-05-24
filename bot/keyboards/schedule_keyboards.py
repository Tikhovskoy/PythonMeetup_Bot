from telegram import ReplyKeyboardMarkup


def get_schedule_keyboard():
    return ReplyKeyboardMarkup(
        [["⬅️ Назад"]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
