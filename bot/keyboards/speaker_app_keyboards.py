from telegram import ReplyKeyboardMarkup


def get_speaker_keyboard():
    return ReplyKeyboardMarkup(
        [["⬅️ Назад"]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def get_speaker_menu_keyboard():
    return ReplyKeyboardMarkup(
        [
            ["📋 Выступаю", "Выступил"],
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )


def get_speaker_menu_speech_keyboard():
    return ReplyKeyboardMarkup(
        [
            ["Вопросы", "Выступил"],
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )