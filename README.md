# PythonMeetup Bot

Telegram-бот для управления офлайн-ивентом **PythonMeetup**.  
Позволяет участникам задавать вопросы спикерам, просматривать программу, делать донаты, участвовать в нетворкинге, подписываться на будущие мероприятия и подавать заявки на выступление. Организаторы получают удобную админ-панель на Django для управления всем процессом.

---

## Возможности

- Регистрация участников и спикеров
- Просмотр расписания и информации о мероприятиях
- Вопросы спикерам во время митапа
- Анкеты для знакомств между участниками
- Донаты на развитие митапа (Telegram Payments)
- Подписка на уведомления о новых мероприятиях
- Заявки на участие в качестве спикера
- Массовые рассылки уведомлений (через админку)
- Администрирование через Django admin

## Структура проекта

```

pythonmeetup/
├── apps/                      # Django-приложения (модули бизнес-логики)
│   └── events/
│
├── bot/                       # Логика Telegram-бота
│   ├── constants.py           # Все FSM-состояния, callback-data, команды
│   ├── persistence.py         # Кастомный Persistence → модель BotState
│   ├── telegram\_bot.py       # Точка входа: Updater, регистрация хендлеров
│   │
│   ├── keyboards/             # inline- и reply-клавиатуры
│   │   ├── main\_menu.py
│   │   ├── qna\_keyboards.py
│   │   ├── networking\_keyboards.py
│   │   ├── donations\_keyboards.py
│   │   ├── subscriptions\_keyboards.py
│   │   └── speaker\_app\_keyboards.py
│   │
│   ├── handlers/              # ConversationHandler и MessageHandler
│   │   ├── start.py
│   │   ├── schedule.py
│   │   ├── qna.py
│   │   ├── networking.py
│   │   ├── donations.py
│   │   ├── subscriptions.py
│   │   └── speaker\_app.py
│   │
│   ├── services/              # Прокси для apps/\*.services
│   │   ├── qna\_service.py
│   │   ├── networking\_service.py
│   │   ├── donation\_service.py
│   │   ├── subscription\_service.py
│   │   └── speaker\_app\_service.py
│   │
│   └── utils/                 # Декораторы, логгер, форматтеры
│       ├── decorators.py
│       ├── logger.py
│       └── formatters.py
│
├── scripts/                   # Вспомогательные утилиты (экспорт CSV, рассылки)
│
├── pythonmeetup/              # Django-конфиг (settings, urls, wsgi, asgi)
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── manage.py                  # Django-команды
├── requirements.txt           # Основные зависимости
├── .env                       # Секреты и переменные окружения
└── .gitignore                 # Файлы и папки, игнорируемые Git

```

---

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone git@github.com:ваш-репозиторий.git
   cd PythonMeetup_Bot
  ```

2. Установите зависимости:

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Укажите переменные окружения в `.env`:

   * `BOT_TOKEN`
   * `PAYMENTS_PROVIDER_TOKEN` (для донатов)
   * другие (DB и т.п.)

4. Проведите миграции и создайте суперпользователя:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. Запустите Django сервер и Telegram-бота:

   ```bash
   python manage.py runserver
   # отдельным процессом:
   python bot/telegram_bot.py
   ```

---

## Описание папок и файлов

* **apps/** — ваши Django-приложения с моделями и сервисами:

  * `core/` — модель `TelegramUser`, `BotState`, общий code.
  * `events/` — `Event`, `Session`, логика программы митапа.
  * `qna/` — `Question`, обработка вопросов.
  * `networking/` — `ParticipantProfile`, `MatchRequest`, matching-алгоритм.
  * `donations/` — модель `Donation`, интеграция платежей.
  * `subscriptions/` — `Subscription`, `SpeakerApplication`.

* **bot/** — вся логика Telegram-бота:

  * `constants.py` — константы FSM и callback-data.
  * `persistence.py` — хранение состояний FSM в модели `BotState`.
  * `telegram_bot.py` — инициализация Updater, регистрация хендлеров.
  * **keyboards/** — фабрики клавиатур.
  * **handlers/** — обработчики команд и диалоговых сценариев.
  * **services/** — прокси-слой, перенаправляет в `apps/.../services.py`.
  * **utils/** — декораторы, логирование, форматирование.

* **scripts/** — скрипты утилиты (CSV-экспорт, массовые рассылки).

* **pythonmeetup/** — директория с настройками Django: `settings.py`, `urls.py`, `wsgi.py`, `asgi.py`.

* **manage.py** — точка входа для Django-команд.

* **requirements.txt** — фиксированные основные зависимости.

* **.env** — ваши секреты и переменные окружения (не коммитить в репозиторий).

* **.gitignore** — правила игнорирования временных и конфиденциальных файлов.