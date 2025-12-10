FROM python:3.13-slim

# Установка зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc python3-dev curl build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY api_yamdb/ ./

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0.0.0.0:8000"]
