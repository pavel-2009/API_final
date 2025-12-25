# YamDB API

[![Tests](https://github.com/YOUR_USERNAME/api_yamdb/workflows/tests/badge.svg)](https://github.com/YOUR_USERNAME/api_yamdb/actions/workflows/tests.yml)

API для базы данных рецензий на произведения (фильмы, книги и музыка).

## Описание

YamDB - это API сервис, который позволяет пользователям:
- Просматривать произведения (фильмы, книги, музыку)
- Добавлять рецензии и оценки
- Оставлять комментарии к рецензиям
- Просматривать рецензии других пользователей

## Технологический стек

- Python 3.9+
- Django 5.2
- Django REST Framework
- PostgreSQL
- Docker
- Docker Compose

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/YOUR_USERNAME/api_yamdb.git
cd api_yamdb
```

2. Установите зависимости:
```bash
pip install -r api_yamdb/requirements.txt
```

3. Выполните миграции:
```bash
cd api_yamdb
python manage.py migrate
```

4. Запустите сервер:
```bash
python manage.py runserver
```

## Docker

Для запуска с использованием Docker:

```bash
cd infra
docker-compose up -d
```

## Тестирование

Запустите тесты:
```bash
pytest tests/
```

## API Документация

После запуска сервера документация доступна по адресу:
- Swagger UI: `http://localhost:8000/api/schema/swagger-ui/`
- ReDoc: `http://localhost:8000/redoc/`

## Автор

Павел Якимович
