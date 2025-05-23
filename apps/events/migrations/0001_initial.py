# Generated by Django 5.2.1 on 2025-05-23 16:35

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Donate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "telegram_id",
                    models.BigIntegerField(
                        blank=True, null=True, verbose_name="Telegram ID"
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="Ф.И.О")),
                (
                    "amount",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="Сумма доната",
                    ),
                ),
                (
                    "created_at",
                    models.DateField(auto_now_add=True, verbose_name="Дата создания"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100, verbose_name="Название")),
                (
                    "description",
                    models.TextField(
                        blank=True, null=True, verbose_name="Описание мероприятия"
                    ),
                ),
                (
                    "start_event",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Начало мероприятия"
                    ),
                ),
                (
                    "end_event",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Конец мероприятия"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Speaker",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="Ф.И.О")),
                (
                    "telegram_id",
                    models.BigIntegerField(
                        blank=True, null=True, verbose_name="Telegram ID"
                    ),
                ),
                (
                    "biography",
                    models.TextField(blank=True, null=True, verbose_name="Биография"),
                ),
                (
                    "created_at",
                    models.DateField(
                        auto_now_add=True, verbose_name="Дата регистрации"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SpeakerApplication",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("telegram_id", models.BigIntegerField(verbose_name="Telegram ID")),
                ("name", models.CharField(max_length=100, verbose_name="Ф.И.О")),
                (
                    "topic",
                    models.CharField(max_length=200, verbose_name="Тема доклада"),
                ),
                (
                    "desc",
                    models.TextField(blank=True, null=True, verbose_name="Описание"),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("new", "Новая"),
                            ("approved", "Одобрена"),
                            ("rejected", "Отклонена"),
                        ],
                        default="new",
                        max_length=20,
                        verbose_name="Статус заявки",
                    ),
                ),
                (
                    "created_at",
                    models.DateField(auto_now_add=True, verbose_name="Дата создания"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Subscription",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("telegram_id", models.BigIntegerField(verbose_name="Telegram ID")),
                ("name", models.CharField(max_length=100, verbose_name="Ф.И.О")),
                (
                    "is_subscribed",
                    models.BooleanField(default=False, verbose_name="Подписка"),
                ),
                (
                    "created_at",
                    models.DateField(
                        auto_now_add=True, verbose_name="Дата регистрации"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "telegram_id",
                    models.BigIntegerField(
                        blank=True, null=True, verbose_name="Telegram ID"
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="Ф.И.О")),
                (
                    "contacts",
                    models.TextField(blank=True, null=True, verbose_name="Контакты"),
                ),
                ("role", models.TextField(blank=True, null=True, verbose_name="Роль")),
                ("stack", models.TextField(blank=True, null=True, verbose_name="Стек")),
                (
                    "grade",
                    models.TextField(blank=True, null=True, verbose_name="Грейд"),
                ),
                (
                    "created_at",
                    models.DateField(
                        auto_now_add=True, verbose_name="Дата регистрации"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SpeakerTalk",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "topic",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=200,
                        verbose_name="Тема доклада",
                    ),
                ),
                (
                    "start_performance",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Начало выступления"
                    ),
                ),
                (
                    "end_performance",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Конец выступления"
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=False, verbose_name="Статус выступления"
                    ),
                ),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="events.event",
                        verbose_name="Мероприятие",
                    ),
                ),
                (
                    "speaker",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="events.speaker",
                        verbose_name="Докладчики",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "telegram_id",
                    models.BigIntegerField(
                        blank=True, null=True, verbose_name="Telegram ID"
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="Ф.И.О")),
                ("question_text", models.TextField(verbose_name="Вопрос")),
                (
                    "is_answered",
                    models.BooleanField(default=False, verbose_name="Ответ"),
                ),
                (
                    "answer_text",
                    models.TextField(blank=True, null=True, verbose_name="Ответ"),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "speaker",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="events.speakertalk",
                        verbose_name="Докладчик",
                    ),
                ),
            ],
        ),
    ]
