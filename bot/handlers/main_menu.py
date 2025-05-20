from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, filters

from bot.handlers.start import start_handler, cancel_handler
from bot.handlers.schedule import schedule_handler, back_to_menu_handler
from bot.handlers.qna import qna_handler
from bot.handlers.networking import networking_handler
from bot.handlers.donations import donate_handler
from bot.handlers.subscriptions import subscribe_handler
from bot.handlers.speaker_app import speaker_app_handler
from bot.constants import STATE_MENU, STATE_SCHEDULE

main_menu_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start_handler)],
    states={
        STATE_MENU: [
            MessageHandler(filters.Regex("^(📋 Программа)$"), schedule_handler),
            MessageHandler(filters.Regex("^(❓ Задать вопрос)$"), qna_handler),
            MessageHandler(filters.Regex("^(🤝 Познакомиться)$"), networking_handler),
            MessageHandler(filters.Regex("^(💰 Донат)$"), donate_handler),
            MessageHandler(filters.Regex("^(🔔 Подписаться)$"), subscribe_handler),
            MessageHandler(filters.Regex("^(🎤 Стать спикером)$"), speaker_app_handler),
        ],
        STATE_SCHEDULE: [
            MessageHandler(filters.Regex("^(⬅️ Назад)$"), back_to_menu_handler),
        ]
    },
    fallbacks=[
        CommandHandler("cancel", cancel_handler)
    ]
)
