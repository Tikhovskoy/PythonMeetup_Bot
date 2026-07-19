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

Compose запускает PostgreSQL, Redis, веб-приложение Django, Telegram-бот и Celery worker.
Рассылки из Django Admin ставятся в очередь Redis и обрабатываются worker отдельно от
веб-приложения. Для каждого получателя сохраняются статус доставки и число попыток;
при временной ошибке отправка повторяется до трёх раз.
