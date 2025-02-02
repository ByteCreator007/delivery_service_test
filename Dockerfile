FROM python:3.10-slim

# Устанавливаем переменные окружения для pip
ENV PIP_DEFAULT_TIMEOUT=120

# Устанавливаем Poetry
RUN pip install poetry

WORKDIR /app

# Копируем файлы Poetry
COPY pyproject.toml poetry.lock* /app/

# Устанавливаем зависимости (включая dev-зависимости)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root --with dev

# Копируем исходный код проекта
COPY . /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
