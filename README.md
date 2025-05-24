# PythonMeetup Bot

**PythonMeetup Bot** — это комплексный Telegram-бот с backend на Django для управления офлайн-ивентами Python-сообщества.
Бот автоматизирует регистрацию, вопросы к спикерам, донаты, нетворкинг, заявки на спикеров и подписки на будущие митапы.

---

## Функциональность

* **Регистрация пользователей и спикеров**
* **Программа мероприятия:** быстрый просмотр расписания и информации о докладах
* **Вопросы докладчикам** прямо через Telegram
* **Нетворкинг:** анкеты и подбор знакомств между участниками
* **Донаты через Telegram Payments**
* **Подписка на уведомления о будущих мероприятиях**
* **Заявки на выступление в качестве спикера**
* **Администрирование через Django admin**
* **Массовые рассылки (через админку или отдельный скрипт)**

---

## Структура проекта

```
PythonMeetup_Bot/
├── apps/                   # Django-приложения (бизнес-логика, модели)
│   └── events/
│
├── bot/                    # Логика Telegram-бота
│   ├── constants.py        # FSM-состояния, команды, callback-data
│   ├── logging_tools.py    # Централизованный логгер (RotatingFileHandler)
│   ├── telegram_bot.py     # Точка входа — запуск бота
│   │
│   ├── handlers/           # Telegram-обработчики (по сценариям)
│   ├── keyboards/          # Фабрики inline/reply-клавиатур
│   ├── services/           # Прокси для бизнес-логики (apps/)
│   └── utils/              # Декораторы, дополнительные инструменты
│
├── scripts/                # Вспомогательные скрипты (рассылки, миграции и т.д.)
│
├── pythonmeetup/           # Django-настройки и маршруты (settings, urls, wsgi, asgi)
│
├── manage.py               # Django-команды
├── requirements.txt        # Зависимости проекта
├── .env                    # Переменные окружения (НЕ коммитить!)
├── .gitignore              # Список игнорируемых файлов/папок
└── README.md               # Описание и инструкция (этот файл)
```

---

## Установка и запуск

1. **Клонируйте репозиторий:**

   ```bash
   git clone <ваш-репозиторий>
   cd PythonMeetup_Bot
   ```

2. **Установите зависимости:**

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Создайте свой `.env`:**

   ```
   BOT_TOKEN=ваш_telegram_token
   PAYMENTS_PROVIDER_TOKEN=токен_платёжной_системы
   # и другие необходимые переменные
   ```

4. **Запустите миграции и создайте администратора Django:**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Запустите Django и бота (двумя разными процессами/терминалами):**

   ```bash
   python manage.py runserver
   python bot/telegram_bot.py
   ```

---

## Основные папки и файлы

* **apps/** — Django-приложения
* **bot/constants.py** — состояния FSM, callback-data, команды.
* **bot/handlers/** — обработчики команд и сценариев (start, schedule, qna, donations, networking, subscriptions, speaker\_app).
* **bot/services/** — прокси для бизнес-логики (`apps/`).
* **bot/keyboards/** — фабрики клавиатур (main\_menu, qna, donations, networking, subscriptions, speaker\_app).
* **bot/logging\_tools.py** — настройка логгирования (вывод в logs/bot.log, ротация файлов, форматирование).
* **bot/utils/** — утилиты, декораторы, форматтеры для сообщений.
* **bot/telegram\_bot.py** — точка входа, регистрация хендлеров, запуск polling.
* **pythonmeetup/** — конфиг Django (settings.py, urls.py, wsgi.py, asgi.py).
* **requirements.txt** — все зависимости проекта.
* **.env.example** — шаблон для ваших переменных окружения.

---

## Переменные окружения (`.env`)

Пример содержимого `.env`:

```
BOT_TOKEN=...
PAYMENTS_PROVIDER_TOKEN=...
```

---

## Логирование

* Все события и ошибки пишутся в файл `logs/bot.log`.
* Используется централизованный логгер (см. `bot/logging_tools.py`).

---

## Тесты

* Для запуска тестов используйте:

  ```bash
  pytest
  ```
* Тесты покрывают обработчики, сервисы, бизнес-логику.

---

## Администрирование

* Вся административная работа (просмотр профилей, заявок, донатов, рассылки) — через стандартную Django admin-панель.
