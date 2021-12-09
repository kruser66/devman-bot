# Уведомления о проверке работ

Модуль позволяет получать уведомления в Телеграм о проверке работ, используя API [Devman](dvmn.org).

После проверки работы предодавателем Вам придет сообщение с информацией:
* Название урока
* Ссылка на проверенный урок
* Принята работа или обнаружены ошибки и нужно переделать

# Как установить

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть есть конфликт с Python2) для установки зависимостей:

```
pip install -r requirements.txt
```

## Пример запуска

```
python devman_bot.py
``` 

## Переменные окружения
Для корректной работы модуля необходимы следующие переменные окружения:

Devman API token взять в разделе "Профиль"
```
DEVMAN_API_TOKEN = 'YOUR_AUTORIZATION_TOKEN'
```
Telegram bot token для своего бота можно узнать у бота `@BotFather`
```
TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
```
Ваш `chat_id` можете узнать у бота `@userinfobot`
```
TELEGRAM_CHAT_ID = YOUR_CHAT_ID
```

# Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [Devman](dvmn.org).
