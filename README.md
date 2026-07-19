# PythonMeetup Bot

Telegram-бот и Django Admin для проведения офлайн-митапов Python-сообщества.
Проект помогает вести расписание, принимать вопросы докладчикам, собирать анкеты
для нетворкинга, получать донаты и управлять рассылками.

## Возможности

- регистрация пользователей бота по команде `/start`;
- программа мероприятия и управление докладами;
- Q&A для активного доклада;
- анкеты и просмотр участников для нетворкинга;
- заявки на выступление и уведомления об их статусе;
- подписки на новости;
- платежи Telegram с проверкой суммы, валюты и защитой от повторной обработки;
- Django Admin для управления данными и рассылками.

## Технологии

- Python 3.12;
- Django 5.2;
- python-telegram-bot;
- PostgreSQL для контейнерного запуска;
- Redis для последующего подключения фоновых задач;
- uv для зависимостей;
- pytest, Ruff, pre-commit и GitHub Actions.

## Архитектура

```text
Telegram ──> bot/handlers ──> bot/services ──> Django models ──> PostgreSQL
                   │                                      │
                   └──────── Django Admin ────────────────┘

Redis используется контейнерным окружением как готовая основа для фоновых задач.
```

`handlers` отвечают за взаимодействие с Telegram, `services` содержат
бизнес-логику, а `apps/events` — модели и административный интерфейс.

## Быстрый запуск через uv

Нужен Python 3.12 и установленный [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/Tikhovskoy/PythonMeetup_Bot.git
cd PythonMeetup_Bot
uv sync --group dev
```

Создайте `.env` на основе `.env.example` и заполните хотя бы `BOT_TOKEN`.

```bash
uv run python manage.py migrate
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

В отдельном терминале запустите бота:

```bash
uv run python -m bot.telegram_bot
```

## Запуск в Docker

Контейнерное окружение включает Django, Telegram-бота, PostgreSQL и Redis.

```bash
copy .env.example .env
docker compose up --build -d
docker compose exec web .venv/bin/python manage.py migrate
docker compose exec web .venv/bin/python manage.py createsuperuser
```

Админка будет доступна по адресу `http://localhost:8000/admin/`.
Подробности — в [инструкции по развёртыванию](docs/deployment.md).

## Переменные окружения

| Переменная | Назначение |
| --- | --- |
| `SECRET_KEY` | секрет Django |
| `DEBUG` | режим отладки (`true` или `false`) |
| `ALLOWED_HOSTS` | разрешённые хосты через запятую |
| `BOT_TOKEN` | токен Telegram-бота |
| `PAYMENTS_PROVIDER_TOKEN` | токен платёжного провайдера Telegram |
| `TELEGRAM_OWNER_ID` | Telegram ID для технических уведомлений |
| `POSTGRES_*` | настройки PostgreSQL |

Полный список приведён в `.env.example`. Не добавляйте `.env` и токены в Git.

## Проверки качества

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest -q
uv run python manage.py makemigrations --check --dry-run
uv run python manage.py check --deploy
```

Перед коммитом можно установить hooks:

```bash
uv run pre-commit install
```

GitHub Actions автоматически выполняет линтинг, проверку форматирования,
миграций и тестов для каждого push и pull request.

## Тестирование Telegram

Используйте отдельного тестового бота. После запуска отправьте ему `/start`:
в Django Admin появится запись в разделе «Пользователи бота». Для платежей
нужен тестовый токен платёжного провайдера Telegram.

## Статус проекта

Проект готов для локального и контейнерного запуска. Для production-развёртывания
следует задать безопасные значения переменных окружения, включить HTTPS и вынести
массовые рассылки в очередь фоновых задач.
