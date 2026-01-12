# Softy — Telegram Mini App для продажи эко-грелок

## Что внутри

- `index.html` — Mini App (красивая страница заказа)
- `bot.py` — Telegram бот
- `app.py` — Flask сервер для хостинга Mini App
- `product.png` — фото товара

## Деплой на Render.com (бесплатно)

### Шаг 1: Загрузите на GitHub

1. Создайте репозиторий на github.com
2. Загрузите все файлы

### Шаг 2: Создайте Web Service для Mini App

1. Зайдите на render.com
2. New → Web Service
3. Подключите репозиторий
4. Настройки:
   - Name: `softy-webapp`
   - Runtime: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
5. Выберите Free план
6. Create Web Service

### Шаг 3: Получите URL

После деплоя вы получите URL типа:
`https://softy-webapp.onrender.com`

### Шаг 4: Обновите бота

Откройте `bot.py` и замените:
```python
WEBAPP_URL = "https://softy-webapp.onrender.com"
```

### Шаг 5: Запустите бота

Бота можно запустить:
- На том же Render (создайте второй Background Worker)
- На своём компьютере
- На другом хостинге

## Настройка

В `bot.py` измените:
- `CARD_NUMBER` — ваш номер карты
- `MANAGER_CHAT_ID` — ваш Chat ID
- `WEBAPP_URL` — URL после деплоя
