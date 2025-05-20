from telegram import ReplyKeyboardMarkup

def get_main_menu_keyboard():
    return ReplyKeyboardMarkup(
        [
            ["📋 Программа", "❓ Задать вопрос"],
            ["🤝 Познакомиться", "💰 Донат"],
            ["🔔 Подписаться", "🎤 Стать спикером"],
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
