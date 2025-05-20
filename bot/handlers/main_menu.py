from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, filters

from bot.handlers.start import start_handler, cancel_handler
from bot.handlers.schedule import schedule_handler, back_to_menu_handler
from bot.handlers.qna import (
    qna_handler, qna_select_speaker_handler, qna_ask_text_handler
)
from bot.handlers.networking import (
    networking_handler,
    netw_name_handler,
    netw_contacts_handler,
    netw_stack_handler,
    netw_role_handler,
    netw_grade_handler,
)
from bot.handlers.donations import donate_handler
from bot.handlers.subscriptions import subscribe_handler
from bot.handlers.speaker_app import speaker_app_handler
from bot.constants import (
    STATE_MENU,
    STATE_SCHEDULE,
    STATE_QNA_SELECT_SPEAKER,
    STATE_QNA_ASK_TEXT,
    STATE_NETW_NAME,
    STATE_NETW_CONTACTS,
    STATE_NETW_STACK,
    STATE_NETW_ROLE,
    STATE_NETW_GRADE,
)

# Все кнопки главного меню и их хендлеры
MENU_BUTTON_HANDLERS = [
    MessageHandler(filters.Regex("^(📋 Программа)$"), schedule_handler),
    MessageHandler(filters.Regex("^(❓ Задать вопрос)$"), qna_handler),
    MessageHandler(filters.Regex("^(🤝 Познакомиться)$"), networking_handler),
    MessageHandler(filters.Regex("^(💰 Донат)$"), donate_handler),
    MessageHandler(filters.Regex("^(🔔 Подписаться)$"), subscribe_handler),
    MessageHandler(filters.Regex("^(🎤 Стать спикером)$"), speaker_app_handler),
]

main_menu_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start_handler)],
    states={
        STATE_MENU: MENU_BUTTON_HANDLERS,
        STATE_SCHEDULE: [
            MessageHandler(filters.Regex("^(⬅️ Назад)$"), back_to_menu_handler),
        ],
        STATE_QNA_SELECT_SPEAKER: MENU_BUTTON_HANDLERS + [
            MessageHandler(filters.TEXT & ~filters.COMMAND, qna_select_speaker_handler),
        ],
        STATE_QNA_ASK_TEXT: MENU_BUTTON_HANDLERS + [
            MessageHandler(filters.TEXT & ~filters.COMMAND, qna_ask_text_handler),
        ],
        STATE_NETW_NAME: MENU_BUTTON_HANDLERS + [
            MessageHandler(filters.TEXT & ~filters.COMMAND, netw_name_handler),
        ],
        STATE_NETW_CONTACTS: MENU_BUTTON_HANDLERS + [
            MessageHandler(filters.TEXT & ~filters.COMMAND, netw_contacts_handler),
        ],
        STATE_NETW_STACK: MENU_BUTTON_HANDLERS + [
            MessageHandler(filters.TEXT & ~filters.COMMAND, netw_stack_handler),
        ],
        STATE_NETW_ROLE: MENU_BUTTON_HANDLERS + [
            MessageHandler(filters.TEXT & ~filters.COMMAND, netw_role_handler),
        ],
        STATE_NETW_GRADE: MENU_BUTTON_HANDLERS + [
            MessageHandler(filters.TEXT & ~filters.COMMAND, netw_grade_handler),
        ],
    },
    fallbacks=[
        CommandHandler("cancel", cancel_handler)
    ]
)
