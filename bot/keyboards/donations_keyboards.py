from telegram import ReplyKeyboardMarkup

DONATE_SUMS = [100, 200, 500, 1000]

def get_donate_keyboard():
    return ReplyKeyboardMarkup(
        [[f"{amount} ₽" for amount in DONATE_SUMS], ["⬅️ Назад"]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

def get_donate_confirm_keyboard(amount):
    return ReplyKeyboardMarkup(
        [[f"{amount} ₽"], ["⬅️ Назад"]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
