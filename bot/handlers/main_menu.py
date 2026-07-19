from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, filters

from bot.constants import (
    STATE_APPLY_DESC,
    STATE_APPLY_FULL_NAME,
    STATE_APPLY_TOPIC,
    STATE_DONATE_CONFIRM,
    STATE_DONATE_INIT,
    STATE_MENU,
    STATE_NETW_CONTACTS,
    STATE_NETW_GRADE,
    STATE_NETW_NAME,
    STATE_NETW_ROLE,
    STATE_NETW_SHOW,
    STATE_NETW_STACK,
    STATE_QNA_ASK_TEXT,
    STATE_SCHEDULE,
    STATE_SUBSCRIBE_CONFIRM,
)
from bot.handlers.donations import (
    donate_cancel_handler,
    donate_handler,
    donate_wait_amount_handler,
    successful_payment_handler,
)
from bot.handlers.networking import (
    netw_contacts_handler,
    netw_grade_handler,
    netw_name_handler,
    netw_role_handler,
    netw_show_handler,
    netw_stack_handler,
    networking_handler,
)
from bot.handlers.qna import qna_ask_text_handler, qna_handler
from bot.handlers.schedule import back_to_menu_handler, schedule_handler
from bot.handlers.speaker import (
    handle_speaker_finish,
    handle_speaker_question,
    handle_speaker_start,
)
from bot.handlers.speaker_app import (
    speaker_app_full_name_handler,
    speaker_app_handler,
    speaker_desc_handler,
    speaker_topic_handler,
)
from bot.handlers.start import cancel_handler, start_handler
from bot.handlers.subscriptions import subscribe_confirm_handler, subscribe_handler

MENU_BUTTON_HANDLERS = [
    MessageHandler(filters.Regex("^(📋 Программа)$"), schedule_handler),
    MessageHandler(filters.Regex("^(❓ Задать вопрос)$"), qna_handler),
    MessageHandler(filters.Regex("^(🤝 Познакомиться)$"), networking_handler),
    MessageHandler(filters.Regex("^(💰 Донат)$"), donate_handler),
    MessageHandler(filters.Regex("^(🔔 Подписка)$"), subscribe_handler),
    MessageHandler(filters.Regex("^(🎤 Стать спикером)$"), speaker_app_handler),
    MessageHandler(filters.Regex("^(📋 Выступаю)$"), handle_speaker_start),
    MessageHandler(filters.Regex("^(Выступил)$"), handle_speaker_finish),
    MessageHandler(filters.Regex("^(Вопросы)$"), handle_speaker_question),
]

main_menu_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start_handler)],
    states={
        STATE_MENU: MENU_BUTTON_HANDLERS,
        STATE_SCHEDULE: [
            MessageHandler(filters.Regex("^(⬅️ Назад)$"), back_to_menu_handler),
        ],
        STATE_QNA_ASK_TEXT: MENU_BUTTON_HANDLERS
        + [
            MessageHandler(filters.TEXT & ~filters.COMMAND, qna_ask_text_handler),
        ],
        STATE_NETW_NAME: MENU_BUTTON_HANDLERS
        + [
            MessageHandler(filters.TEXT & ~filters.COMMAND, netw_name_handler),
        ],
        STATE_NETW_CONTACTS: MENU_BUTTON_HANDLERS
        + [
            MessageHandler(filters.TEXT & ~filters.COMMAND, netw_contacts_handler),
        ],
        STATE_NETW_STACK: MENU_BUTTON_HANDLERS
        + [
            MessageHandler(filters.TEXT & ~filters.COMMAND, netw_stack_handler),
        ],
        STATE_NETW_ROLE: MENU_BUTTON_HANDLERS
        + [
            MessageHandler(filters.TEXT & ~filters.COMMAND, netw_role_handler),
        ],
        STATE_NETW_GRADE: MENU_BUTTON_HANDLERS
        + [
            MessageHandler(filters.TEXT & ~filters.COMMAND, netw_grade_handler),
        ],
        "DONATE_WAIT_AMOUNT": [
            MessageHandler(filters.Regex("^⬅️ Назад$"), donate_cancel_handler),
            MessageHandler(filters.TEXT & ~filters.COMMAND, donate_wait_amount_handler),
        ],
        "DONATE_WAIT_PAYMENT": [
            MessageHandler(filters.Regex("^⬅️ Назад$"), donate_cancel_handler),
            MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_handler),
        ],
        STATE_DONATE_INIT: MENU_BUTTON_HANDLERS + [],
        STATE_DONATE_CONFIRM: MENU_BUTTON_HANDLERS + [],
        STATE_SUBSCRIBE_CONFIRM: MENU_BUTTON_HANDLERS
        + [
            MessageHandler(filters.TEXT & ~filters.COMMAND, subscribe_confirm_handler),
        ],
        STATE_APPLY_FULL_NAME: MENU_BUTTON_HANDLERS
        + [
            MessageHandler(filters.TEXT & ~filters.COMMAND, speaker_app_full_name_handler),
        ],
        STATE_APPLY_TOPIC: MENU_BUTTON_HANDLERS
        + [
            MessageHandler(filters.TEXT & ~filters.COMMAND, speaker_topic_handler),
        ],
        STATE_APPLY_DESC: MENU_BUTTON_HANDLERS
        + [
            MessageHandler(filters.TEXT & ~filters.COMMAND, speaker_desc_handler),
        ],
        STATE_NETW_SHOW: [
            MessageHandler(
                filters.Regex("^(➡️ Дальше|🔄 Начать сначала|⬅️ В меню)$"),
                netw_show_handler,
            ),
        ],
    },
    fallbacks=[
        CommandHandler("cancel", cancel_handler),
        CommandHandler("start", start_handler),
    ],
)
