# Product-Tracker-Bot
Бот, который помогает следить за учетом товаров на полках магазинов

## Локальный запуск

1. Склонируйте репозиторий:
```bash
git clone <адрес репозитория>
cd <папка проекта>
```

2. Создайте файл .env в корне проекта и заполните его переменными окружения:

- Токен бота
- Токен perfume-backend
- Данные для входа в supabase

3. Установить зависимости:
```bash
pip install -r requirements.txt
```

4. Запустить программу:
```bash
python -m app.main
```

После загрузки всех логов можно переходить в Telegram и тестировать бота

## Запуск через Docker

1. Соберите Docker-образ
```bash
docker build -t product-tracker-bot .
```

2. Запустите контейнер
```bash
docker run --env-file .env product-tracker-bot
```

Для запуска в фоновом режиме:
```bash
docker run -d --env-file .env --name tracker-bot product-tracker-bot
```

Для остановки контейнера:
```bash
docker stop tracker-bot
```

## Требования

- Python 3.10 или выше
- Docker (если используете контейнеризацию)
- Все зависимости из requirements.txt
