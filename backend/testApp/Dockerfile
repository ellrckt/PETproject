FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="$VIRTUAL_ENV/bin:$PATH" \
    APP_HOME=/app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv $VIRTUAL_ENV

WORKDIR $APP_HOME
ENV PYTHONPATH="/app"
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser $APP_HOME $VIRTUAL_ENV

COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000

# HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
#     CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000