from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import BadRequest

from bot.constants import STATE_MENU, STATE_QNA_ANSWER_QUESTION
from bot.keyboards.speaker_app_keyboards import (
    get_speaker_menu_keyboard,
    get_speaker_menu_speech_keyboard,
    get_speaker_answers_questions_keyboard,
    get_no_questions_keyboard
)
from bot.services import speaker_service


async def handle_speaker_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    now = datetime.now()
    context.user_data["is_speaking"] = True
    speaker_id = update.effective_user.id
    speaker_service.start_performance(speaker_id)
    # запись в БД
    print(f"{user_name} начал выступление в {now}")

    # TODO: если по таймингу выступление началось?
    await update.message.reply_text(
        "Ты начал выступление! Теперь ты можешь просматривать вопросы.",
        reply_markup=get_speaker_menu_speech_keyboard()
    )
    return STATE_MENU


async def handle_speaker_finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    now = datetime.now()
    context.user_data["is_speaking"] = False
    speaker_id = update.effective_user.id
    speaker_service.finish_performance(speaker_id)
    # запись в БД
    print(f"{user_name} закончил выступление в {now}")

    await update.message.reply_text(
        "Спасибо за выступление! Ждём тебя снова.",
        reply_markup=get_speaker_menu_keyboard()
    )
    return STATE_MENU


async def handle_speaker_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    speaker_id = update.effective_user.id
    questions = speaker_service.get_questions_for_speaker(speaker_id)
    # Получить из Бд вопросы
    unanswered = [question for question in questions if not question["answered"]]
    if not unanswered:
        await update.message.reply_text("Пока нет новых вопросов.")
        return STATE_MENU

    await update.message.reply_text(
        "Выберите номер вопроса, на который хотите ответить:",
        reply_markup=get_speaker_answers_questions_keyboard(unanswered)
    )
    return STATE_QNA_ANSWER_QUESTION


async def qna_receive_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    speaker_id = update.effective_user.id
    questions = speaker_service.get_questions_for_speaker(speaker_id)
    user_input = update.message.text
    if user_input == "⬅️ Назад":
        await update.message.reply_text(
            "Возврат на шаг назад.",
            reply_markup=get_speaker_menu_speech_keyboard()
        )
        context.user_data.pop("current_question", None)
        return STATE_MENU

    current_question = context.user_data.get("current_question")
    if current_question is None:
        question = next((answer for answer in questions if answer["text"] == user_input and not answer["answered"]), None)
        if question is None:
            await update.message.reply_text("Пожалуйста, выберите вопрос из списка или нажмите '⬅️ Назад'.")
            return STATE_QNA_ANSWER_QUESTION

        context.user_data["current_question"] = question
        await update.message.reply_text(f"Введите ответ на вопрос:\n{question['text']}")
        return STATE_QNA_ANSWER_QUESTION

    else:
        answer = user_input
        question = current_question
        user_id = question["user_id"]
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=f"Ответ на ваш вопрос:\n{answer}",
            )
            question["answered"] = True
            context.user_data.pop("current_question", None)
        except BadRequest as e:
            if "chat not found" in str(e).lower():
                await update.message.reply_text(
                    "Не удалось отправить ответ: пользователь не начал диалог с ботом или заблокировал его."
                )
            else:
                raise

        unanswered = [unanswer for unanswer in questions if not unanswer["answered"]]
        if unanswered:
            await update.message.reply_text(
                "Выберите следующий вопрос или вернитесь назад:",
                reply_markup=get_speaker_answers_questions_keyboard(unanswered)
            )
            return STATE_QNA_ANSWER_QUESTION
        else:
            await update.message.reply_text(
                "Все вопросы отвечены.",
                reply_markup=get_no_questions_keyboard()
            )
            return STATE_MENU


async def handler_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Действие отменено.")
    return STATE_MENU
