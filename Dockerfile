FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . .

RUN groupadd --system app && useradd --system --gid app app && chown -R app:app /app

USER app

CMD [".venv/bin/python", "manage.py", "runserver", "0.0.0.0:8000"]
