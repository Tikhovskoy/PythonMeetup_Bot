from telegram import ReplyKeyboardMarkup

def get_subscribe_keyboard():
    return ReplyKeyboardMarkup(
        [["✅ Подписаться", "⬅️ Назад"]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
