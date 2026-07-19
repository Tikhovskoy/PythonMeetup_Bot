# Запуск в контейнерах

1. Скопируйте `.env.example` в `.env` и заполните секреты Telegram.
2. Запустите сервисы:

   ```bash
   docker compose up --build -d
   ```

3. Примените миграции и создайте администратора:

   ```bash
   docker compose exec web .venv/bin/python manage.py migrate
   docker compose exec web .venv/bin/python manage.py createsuperuser
   ```

Django Admin будет доступен по адресу `http://localhost:8000/admin/`.

Compose запускает PostgreSQL, Redis, веб-приложение Django и Telegram-бот. Redis
подготовлен для подключения фоновых задач и не хранит прикладные данные бота.
