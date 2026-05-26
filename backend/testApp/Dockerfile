# syntax=docker/dockerfile:1.4
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    VIRTUAL_ENV=/opt/venv \
    PATH="$VIRTUAL_ENV/bin:$PATH" \
    APP_HOME=/app \
    PYTHONPATH="/app"

# Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Создание venv
RUN python -m venv $VIRTUAL_ENV

WORKDIR $APP_HOME

# Создание пользователя (для безопасности)
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser $APP_HOME $VIRTUAL_ENV

# 🔹 Копируем ТОЛЬКО файлы зависимостей ПЕРЕД кодом приложения
COPY requirements-base.txt .
COPY requirements-ml.txt .

# 🔹 Кэшируем pip через BuildKit mount (ускоряет повторные сборки)
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements-base.txt

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements-ml.txt

# 🔹 Копируем код приложения ПОСЛЕ установки зависимостей
# Если изменится код — слои с pip останутся в кэше!
COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000

CMD ["/bin/sh", "-c", "/opt/venv/bin/python -m alembic upgrade head && /opt/venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8000"]
