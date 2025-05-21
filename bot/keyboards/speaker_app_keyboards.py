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
            ["📋 Выступаю", "⬅️ Назад"],
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


def get_speaker_answers_questions_keyboard(unanswered):
    keyboard = [[q["text"]] for q in unanswered]
    keyboard.append(["⬅️ Назад"])
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )


def get_no_questions_keyboard():
    return ReplyKeyboardMarkup(
        [
            ["Выступил"], ["⬅️ Назад"],
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )


def get_speaker_or_user_keyboard():
    return ReplyKeyboardMarkup(
        [
            ["Войти как докладчик", "Войти как пользователь"]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
