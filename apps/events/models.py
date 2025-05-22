from django.core.validators import MinValueValidator
from django.db import models


class Speaker(models.Model):
    name = models.CharField(verbose_name='Ф.И.О', max_length=100)
    telegram_id = models.BigIntegerField(verbose_name='Telegram ID', null=True, blank=True)
    biography = models.TextField(verbose_name='Биография', null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата регистрации')

    def __str__(self):
        return f'Спикер {self.name}'


class Event(models.Model):
    title = models.CharField(verbose_name='Название', max_length=100)
    description = models.TextField(verbose_name='Описание мероприятия', null=True, blank=True)
    start_event = models.DateTimeField(verbose_name='Начало мероприятия', null=True, blank=True)
    end_event = models.DateTimeField(verbose_name='Конец мероприятия', null=True, blank=True)

    def __str__(self):
        return self.title


class SpeakerTalk(models.Model):
    speaker = models.ForeignKey(Speaker, on_delete=models.CASCADE, verbose_name='Докладчики')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Мероприятие')
    status = models.BooleanField(default=False, verbose_name='Статус выступления')
    start_performance = models.DateTimeField(verbose_name='Начало выступления', null=True, blank=True)
    end_performance = models.DateTimeField(verbose_name='Конец выступления', null=True, blank=True)

    def __str__(self):
        return self.speaker.name


class UserProfile(models.Model):
    telegram_id = models.BigIntegerField(verbose_name='Telegram ID', null=True, blank=True)
    name = models.CharField(verbose_name='Ф.И.О', max_length=100)
    contacts = models.TextField(verbose_name='Контакты', null=True, blank=True)
    role = models.TextField(verbose_name='Роль', null=True, blank=True)
    stack = models.TextField(verbose_name='Стек', null=True, blank=True)
    grade = models.TextField(verbose_name='Грейд', null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата регистрации')

    def __str__(self):
      return f'Анкета {self.name}'


class Question(models.Model):
    telegram_id = models.BigIntegerField(verbose_name='Telegram ID', null=True, blank=True)
    name = models.CharField(verbose_name='Ф.И.О', max_length=100)
    speaker = models.ForeignKey(SpeakerTalk, on_delete=models.CASCADE, verbose_name='Докладчик')
    question_text = models.TextField(verbose_name='Вопрос')
    is_answered = models.BooleanField(default=False, verbose_name='Ответ')
    answer_text = models.TextField(verbose_name='Ответ', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
      return f'Вопрос от {self.name}'


class Donate(models.Model):
    telegram_id = models.BigIntegerField(verbose_name='Telegram ID', null=True, blank=True)
    name = models.CharField(verbose_name='Ф.И.О', max_length=100)
    amount = models.IntegerField(verbose_name='Сумма доната', validators=[MinValueValidator(1)])
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата регистрации')

    def __str__(self):
      return f'Донат от {self.name}'
