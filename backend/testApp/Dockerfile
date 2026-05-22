# ==========================================
# ЭТАП 1: Сборка зависимостей (Builder)
# ==========================================
FROM python:3.13-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="$VIRTUAL_ENV/bin:$PATH"

# Устанавливаем инструменты сборки (нужны только здесь)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv $VIRTUAL_ENV

WORKDIR /build

# Кэшируем и устанавливаем пакеты
COPY requirements-base.txt requirements-ml.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements-base.txt && \
    pip install --no-cache-dir -r requirements-ml.txt

# ==========================================
# ЭТАП 2: Финальный минимальный образ
# ==========================================
FROM python:3.13-slim AS runner

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="$VIRTUAL_ENV/bin:$PATH" \
    APP_HOME=/app \
    PYTHONPATH="/app"

# Для работы asyncpg/psycopg2 в рантайме нужна только базовая libpq5 (без gcc и заголовков)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR $APP_HOME

# Создаем безопасного пользователя
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser $APP_HOME

# СКОПИРОВАНИЕ: Переносим готовое окружение из этапа builder
COPY --from=builder --chown=appuser:appuser /opt/venv /opt/venv

# КОПИРОВАНИЕ: Переносим код приложения (сбросит кэш только для этого слоя)
COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000

CMD ["/bin/sh", "-c", "/opt/venv/bin/python -m alembic upgrade head && /opt/venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8000"]