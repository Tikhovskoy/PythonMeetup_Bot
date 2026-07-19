import uuid

from django.core.validators import MinValueValidator
from django.db import models


class Speaker(models.Model):
    name = models.CharField(verbose_name="Ф.И.О", max_length=100)
    telegram_id = models.BigIntegerField(verbose_name="Telegram ID", unique=True)
    biography = models.TextField(verbose_name="Биография", null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата регистрации")

    class Meta:
        verbose_name = "Спикер"
        verbose_name_plural = "Спикеры"

    def __str__(self):
        return f"Спикер {self.name}"


class Event(models.Model):
    title = models.CharField(verbose_name="Название", max_length=100)
    description = models.TextField(verbose_name="Описание мероприятия", null=True, blank=True)
    start_event = models.DateTimeField(verbose_name="Начало мероприятия", null=True, blank=True)
    end_event = models.DateTimeField(verbose_name="Конец мероприятия", null=True, blank=True)

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"

    def __str__(self):
        return self.title


class SpeakerTalk(models.Model):
    speaker = models.ForeignKey(Speaker, on_delete=models.CASCADE, verbose_name="Докладчики")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="Мероприятие")
    topic = models.CharField(verbose_name="Тема доклада", max_length=200, blank=True, default="")
    start_performance = models.DateTimeField(
        verbose_name="Начало выступления", null=True, blank=True
    )
    end_performance = models.DateTimeField(verbose_name="Конец выступления", null=True, blank=True)
    is_active = models.BooleanField(default=False, verbose_name="Статус выступления")

    def __str__(self):
        return f"{self.speaker.name}: {self.topic or 'Без темы'}"


class UserProfile(models.Model):
    telegram_id = models.BigIntegerField(
        verbose_name="Telegram ID", null=True, blank=True, unique=True
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


class BotUser(models.Model):
    telegram_id = models.BigIntegerField(unique=True, verbose_name="Telegram ID")
    name = models.CharField(max_length=100, verbose_name="Имя")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Пользователь бота"
        verbose_name_plural = "Пользователи бота"

    def __str__(self):
        return f"{self.name} ({self.telegram_id})"


class Question(models.Model):
    telegram_id = models.BigIntegerField(verbose_name="Telegram ID", null=True, blank=True)
    name = models.CharField(verbose_name="Ф.И.О", max_length=100)
    speaker = models.ForeignKey(SpeakerTalk, on_delete=models.CASCADE, verbose_name="Докладчик")
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
    telegram_id = models.BigIntegerField(verbose_name="Telegram ID", null=True, blank=True)
    name = models.CharField(verbose_name="Ф.И.О", max_length=100)
    amount = models.IntegerField(verbose_name="Сумма доната", validators=[MinValueValidator(1)])
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Донат"
        verbose_name_plural = "Донаты"

    def __str__(self):
        return f"Донат от {self.name}"


class Subscription(models.Model):
    telegram_id = models.BigIntegerField(verbose_name="Telegram ID", unique=True)
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

    group = models.CharField(max_length=10, choices=GROUP_CHOICES, verbose_name="Целевая группа")
    message = models.TextField(verbose_name="Текст сообщения")
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name="Время отправки")
    is_sent = models.BooleanField(default=False, verbose_name="Отправлено")
    delivered_count = models.PositiveIntegerField(default=0, verbose_name="Доставлено")
    failed_count = models.PositiveIntegerField(default=0, verbose_name="Ошибки доставки")

    class Meta:
        verbose_name = "Рассылка сообщения"
        verbose_name_plural = "Рассылка сообщений"

    def __str__(self):
        return f"Рассылка для {self.get_group_display()} ({self.sent_at})"


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


class Payment(models.Model):
    STATUS_PENDING = "pending"
    STATUS_PAID = "paid"
    STATUS_CHOICES = [(STATUS_PENDING, "Ожидает оплаты"), (STATUS_PAID, "Оплачен")]

    payload = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    telegram_id = models.BigIntegerField()
    amount = models.PositiveIntegerField()
    currency = models.CharField(max_length=3)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    telegram_payment_charge_id = models.CharField(
        max_length=255, unique=True, null=True, blank=True
    )
    donation = models.OneToOneField(Donate, on_delete=models.PROTECT, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)
