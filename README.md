# PythonMeetup Bot

Telegram-бот для управления офлайн-ивентом **PythonMeetup**.  
Позволяет участникам задавать вопросы спикерам, просматривать программу, делать донаты, участвовать в нетворкинге, подписываться на будущие мероприятия и подавать заявки на выступление. Организаторы получают удобную админ-панель на Django для управления всем процессом.

---

## Структура проекта

```

pythonmeetup/
├── apps/                      # Django-приложения (модули бизнес-логики)
│   ├── core/                  # Пользователи, FSM-состояния
│   ├── events/                # Митапы и сессии (программа)
│   ├── qna/                   # Вопросы к спикерам
│   ├── networking/            # Анкеты участников и matching
│   ├── donations/             # Донаты организаторам
│   └── subscriptions/         # Подписки на митапы и заявки спикеров
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

## Быстрый старт

1. Клонировать репозиторий и перейти в папку:
   
   ```bash
   git clone <url>
   cd pythonmeetup
   ```

2. Создать и активировать виртуальное окружение:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Установить зависимости:

   ```bash
   pip install -r requirements.txt
   ```

4. Настроить `.env` (пример ниже):

   ```ini
   SECRET_KEY=ваш_секрет
   DATABASE_URL=postgres://user:pass@localhost:5432/pythonmeetup
   BOT_TOKEN=123456:ABC-DEF...
   ```

5. Выполнить миграции и создать суперпользователя:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. Запустить сервер Django:

   ```bash
   python manage.py runserver
   ```

7. Запустить бота:

   ```bash
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
````
