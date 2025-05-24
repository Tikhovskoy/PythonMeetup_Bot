from telegram import ReplyKeyboardMarkup


def get_next_profile_keyboard():
    return ReplyKeyboardMarkup(
        [
            ["➡️ Дальше"],
            ["🔄 Начать сначала", "⬅️ В меню"]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def get_profiles_finished_keyboard():
    return ReplyKeyboardMarkup(
        [
            ["🔄 Начать сначала", "⬅️ В меню"]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
