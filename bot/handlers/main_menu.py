from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, filters

from bot.handlers.start import start_handler, cancel_handler, choose_mode_handler
from bot.handlers.speaker import (
    handle_speaker_start,
    handle_speaker_finish,
    handle_speaker_question,
    qna_receive_answer,
    handler_cancel,
    )
from bot.handlers.schedule import schedule_handler, back_to_menu_handler
from bot.handlers.qna import (
    qna_handler, qna_ask_text_handler
)
from bot.handlers.networking import (
    networking_handler,
    netw_name_handler,
    netw_contacts_handler,
    netw_stack_handler,
    netw_role_handler,
    netw_grade_handler,
    netw_show_handler,
)
from bot.handlers.donations import (
    donate_handler,
    donate_wait_amount_handler,
    donate_cancel_handler,
    successful_payment_handler,
)
from bot.handlers.subscriptions import subscribe_handler, subscribe_confirm_handler
from bot.handlers.speaker_app import (
    speaker_app_handler,
    speaker_topic_handler,
    speaker_desc_handler,
)
from bot.constants import (
    STATE_MENU,
    STATE_SCHEDULE,
    STATE_QNA_ASK_TEXT,
    STATE_NETW_NAME,
    STATE_NETW_CONTACTS,
    STATE_NETW_STACK,
    STATE_NETW_ROLE,
    STATE_NETW_GRADE,
    STATE_DONATE_INIT,
    STATE_DONATE_CONFIRM,
    STATE_SUBSCRIBE_CONFIRM,
    STATE_APPLY_TOPIC,
    STATE_APPLY_DESC,
    STATE_QNA_ANSWER_QUESTION,
    STATE_NETW_SHOW,
)

MENU_BUTTON_HANDLERS = [
    MessageHandler(filters.Regex("^(📋 Программа)$"), schedule_handler),
    MessageHandler(filters.Regex("^(❓ Задать вопрос)$"), qna_handler),
    MessageHandler(filters.Regex("^(🤝 Познакомиться)$"), networking_handler),
    MessageHandler(filters.Regex("^(💰 Донат)$"), donate_handler),
    MessageHandler(filters.Regex("^(🔔 Подписаться)$"), subscribe_handler),
    MessageHandler(filters.Regex("^(🎤 Стать спикером)$"), speaker_app_handler),

    MessageHandler(filters.Regex("^(📋 Выступаю)$"), handle_speaker_start),
    MessageHandler(filters.Regex("^(Выступил)$"), handle_speaker_finish),
    MessageHandler(filters.Regex("^(Вопросы)$"), handle_speaker_question),
    MessageHandler(filters.Regex("^(Войти как докладчик|Войти как пользователь|⬅️ Назад)$"), choose_mode_handler),
]

main_menu_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start_handler)],
    states={
        STATE_MENU: MENU_BUTTON_HANDLERS,
        STATE_SCHEDULE: [
            MessageHandler(filters.Regex("^(⬅️ Назад)$"), back_to_menu_handler),
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
        STATE_SUBSCRIBE_CONFIRM: MENU_BUTTON_HANDLERS + [
            MessageHandler(filters.TEXT & ~filters.COMMAND, subscribe_confirm_handler),
        ],
        STATE_APPLY_TOPIC: MENU_BUTTON_HANDLERS + [
            MessageHandler(filters.TEXT & ~filters.COMMAND, speaker_topic_handler),
        ],
        STATE_APPLY_DESC: MENU_BUTTON_HANDLERS + [
            MessageHandler(filters.TEXT & ~filters.COMMAND, speaker_desc_handler),
        ],
        STATE_QNA_ANSWER_QUESTION: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, qna_receive_answer),
            MessageHandler(filters.Regex("^Отмена$"), handler_cancel)],
        STATE_NETW_SHOW: [
            MessageHandler(filters.Regex("^(➡️ Дальше|🔄 Начать сначала|⬅️ В меню)$"), netw_show_handler),
        ],
    },
    fallbacks=[
        CommandHandler("cancel", cancel_handler),
    ]
)
