from django.core.validators import MinValueValidator
from django.db import models

from bot.services.send_message_service import send_telegram_message


class Speaker(models.Model):
    name = models.CharField(verbose_name="Ф.И.О", max_length=100)
    telegram_id = models.BigIntegerField(
        verbose_name="Telegram ID", null=False, blank=False
    )
    biography = models.TextField(verbose_name="Биография", null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата регистрации")

    class Meta:
        verbose_name = "Спикер"
        verbose_name_plural = "Спикеры"

    def __str__(self):
        return f"Спикер {self.name}"


class Event(models.Model):
    title = models.CharField(verbose_name="Название", max_length=100)
    description = models.TextField(
        verbose_name="Описание мероприятия", null=True, blank=True
    )
    start_event = models.DateTimeField(
        verbose_name="Начало мероприятия", null=True, blank=True
    )
    end_event = models.DateTimeField(
        verbose_name="Конец мероприятия", null=True, blank=True
    )

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"

    def __str__(self):
        return self.title


class SpeakerTalk(models.Model):
    speaker = models.ForeignKey(
        Speaker, on_delete=models.CASCADE, verbose_name="Докладчики"
    )
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, verbose_name="Мероприятие"
    )
    topic = models.CharField(
        verbose_name="Тема доклада", max_length=200, blank=True, default=""
    )
    start_performance = models.DateTimeField(
        verbose_name="Начало выступления", null=True, blank=True
    )
    end_performance = models.DateTimeField(
        verbose_name="Конец выступления", null=True, blank=True
    )
    is_active = models.BooleanField(default=False, verbose_name="Статус выступления")

    def __str__(self):
        return f"{self.speaker.name}: {self.topic or 'Без темы'}"


class UserProfile(models.Model):
    telegram_id = models.BigIntegerField(
        verbose_name="Telegram ID", null=True, blank=True
    )
    name = models.CharField(verbose_name="Ф.И.О", max_length=100)
    contacts = models.TextField(verbose_name="Контакты", null=True, blank=True)
    role = models.TextField(verbose_name="Роль", null=True, blank=True)
    stack = models.TextField(verbose_name="Стек", null=True, blank=True)
    grade = models.TextField(verbose_name="Грейд", null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата регистрации")

    class Meta:
        verbose_name = "Анкета слушателя"
        verbose_name_plural = "Анкеты слушателей"

    def __str__(self):
        return f"Анкета {self.name}"


class Question(models.Model):
    telegram_id = models.BigIntegerField(
        verbose_name="Telegram ID", null=True, blank=True
    )
    name = models.CharField(verbose_name="Ф.И.О", max_length=100)
    speaker = models.ForeignKey(
        SpeakerTalk, on_delete=models.CASCADE, verbose_name="Докладчик"
    )
    question_text = models.TextField(verbose_name="Вопрос")
    is_answered = models.BooleanField(default=False, verbose_name="Ответ")
    answer_text = models.TextField(verbose_name="Ответ", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Вопрос к спикеру"
        verbose_name_plural = "Вопросы к спикерам"

    def __str__(self):
        return f"Вопрос от {self.name}"


class Donate(models.Model):
    telegram_id = models.BigIntegerField(
        verbose_name="Telegram ID", null=True, blank=True
    )
    name = models.CharField(verbose_name="Ф.И.О", max_length=100)
    amount = models.IntegerField(
        verbose_name="Сумма доната", validators=[MinValueValidator(1)]
    )
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Донат"
        verbose_name_plural = "Донаты"

    def __str__(self):
        return f"Донат от {self.name}"


class Subscription(models.Model):
    telegram_id = models.BigIntegerField(verbose_name="Telegram ID")
    name = models.CharField(verbose_name="Ф.И.О", max_length=100)
    is_subscribed = models.BooleanField(verbose_name="Подписка", default=False)
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата регистрации")

    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"

    def __str__(self):
        return f"Подписчик {self.name}"


class SendMessage(models.Model):
    GROUP_CHOICES = [
        ("speakers", "Докладчики"),
        ("listeners", "Слушатели"),
        ("all", "Все"),
    ]

    group = models.CharField(
        max_length=10, choices=GROUP_CHOICES, verbose_name="Целевая группа"
    )
    message = models.TextField(verbose_name="Текст сообщения")
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name="Время отправки")
    is_sent = models.BooleanField(default=False, verbose_name="Отправлено")

    class Meta:
        verbose_name = "Рассылка сообщения"
        verbose_name_plural = "Рассылка сообщений"

    def __str__(self):
        return f"Рассылка для {self.get_group_display()} ({self.sent_at})"

    def send_messages(self):
        if self.is_sent:
            return
        telegram_ids = []

        if self.group == "speakers" or self.group == "all":
            speakers_ids = Speaker.objects.values_list("telegram_id", flat=True)
            telegram_ids.extend(speakers_ids)

        if self.group == "listeners" or self.group == "all":
            listeners_ids = UserProfile.objects.values_list("telegram_id", flat=True)
            telegram_ids.extend(listeners_ids)

        unique_ids = list(set(telegram_ids))

        for chat_id in unique_ids:
            send_telegram_message(chat_id, self.message)

        self.is_sent = True
        self.save(update_fields=["is_sent"])


class SpeakerApplication(models.Model):
    STATUS_CHOICES = [
        ("new", "Новая"),
        ("approved", "Одобрена"),
        ("rejected", "Отклонена"),
    ]

    telegram_id = models.BigIntegerField(verbose_name="Telegram ID")
    name = models.CharField(verbose_name="Ф.И.О", max_length=100)
    topic = models.CharField(verbose_name="Тема доклада", max_length=200)
    desc = models.TextField(verbose_name="Описание", null=True, blank=True)
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=20,
        default="new",
        verbose_name="Статус заявки",
    )
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Заявка от спикера"
        verbose_name_plural = "Заявки от спикеров"

    def __str__(self):
        return f"Заявка от {self.name}"

    def save(self, *args, **kwargs):
        send_notification = False
        old_status = None
        if self.pk:
            prev = SpeakerApplication.objects.get(pk=self.pk)
            old_status = prev.status
            if old_status == "new" and self.status != "new":
                send_notification = True
        super().save(*args, **kwargs)
        if send_notification:
            if self.status == "approved":
                text = (
                    f"Ваша заявка на роль спикера ('{self.topic}') ОДОБРЕНА!\n"
                    "С вами свяжутся организаторы для подтверждения участия."
                )
            elif self.status == "rejected":
                text = (
                    f"Ваша заявка на роль спикера ('{self.topic}') ОТКЛОНЕНА.\n"
                    "Спасибо за интерес, приглашаем вас подать заявку в следующий раз!"
                )
            else:
                text = f"Статус вашей заявки на спикера изменён на: {self.get_status_display()}"
            send_telegram_message(self.telegram_id, text)
