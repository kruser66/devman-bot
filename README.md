# Уведомления о проверке работ

Модуль позволяет получать уведомления в Телеграм о проверке работ, используя API [Devman](dvmn.org).

После проверки работы преподавателем Вам придет сообщение с информацией:

* Название урока
* Ссылка на проверенный урок
* Принята работа или обнаружены ошибки и нужно переделать

## Как установить

Python3 должен быть уже установлен. Затем используйте pip (или pip3, если есть конфликт с Python2) для установки зависимостей:

```bash
pip install -r requirements.txt
```

## Пример запуска

```bash
python devman_bot.py
```

## Переменные окружения

Для корректной работы модуля необходимы следующие переменные окружения:

```python
DEVMAN_API_TOKEN='YOUR_AUTORIZATION_TOKEN'
TELEGRAM_BOT_TOKEN='YOUR_TELEGRAM_BOT_TOKEN'
TELEGRAM_CHAT_ID='YOUR_CHAT_ID'
```

## Docker

1. Создание образа.

Находясь в каталоге проекта запустите:

```bash
docker build --tag devman_bot .
```

2. Запуск контейнера.

* с указание переменных окружения в командной строке:

```bash
docker run -d \ 
-e DEVMAN_API_TOKEN='YOUR_AUTORIZATION_TOKEN' \
-e TELEGRAM_BOT_TOKEN='YOUR_TELEGRAM_BOT_TOKEN' \
-e TELEGRAM_CHAT_ID='YOUR_CHAT_ID' \ 
--name container_name kruser66/devman_bot
```

* создайте файл `.env` с перемнными окружения:

```bash
docker run -d --env-file .env --name container_name kruser66/devman_bot
```

## Цель проекта

Код написан в образовательных целях на онлайн-курс для веб-разработчиков [Devman](dvmn.org).
