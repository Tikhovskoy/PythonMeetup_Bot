from telegram import ReplyKeyboardMarkup

def get_subscribe_keyboard(is_subscribed: bool = False):
    """
    Генерирует клавиатуру для подписки/отписки.
    """
    if is_subscribed:
        buttons = [["❌ Отписаться", "⬅️ Назад"]]
    else:
        buttons = [["✅ Подписаться", "⬅️ Назад"]]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
