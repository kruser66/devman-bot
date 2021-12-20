import os
import requests
import logging
import telegram
from time import sleep
from dotenv import load_dotenv

logger = logging.getLogger("Телеграм_логгер")


def bot_send_messages(bot, chat_id, server_answer):

    for attempt in server_answer['new_attempts']:
        title = 'У Вас проверили работу:\n"{}"'.format(attempt['lesson_title'])
        if attempt['is_negative']:
            correct = '_К сожалению, в работе нашлись ошибки_'
        else:
            correct = '''
            _Преподавателю все понравилось\n
            Можете приступать к следующему заданию_
            '''
        link = '[Ссылка на Вашу работу]({})'.format(attempt['lesson_url'])
        bot.send_message(
            chat_id=chat_id,
            text=f'{title}\n\n{link}\n\n{correct}',
            parse_mode=telegram.ParseMode.MARKDOWN_V2
        )


def long_polling(token, params, bot, chat_id, timeout=90):
    api_url = 'https://dvmn.org/api/long_polling/'

    headers = {
        'Authorization': token,
    }

    while True:
        response = requests.get(
            api_url,
            headers=headers,
            params=params,
            timeout=timeout
        )
        response.raise_for_status()
        checking = response.json()

        if checking['status'] == 'timeout':
            params['timestamp'] = checking['timestamp_to_request']
        elif checking['status'] == 'found':
            bot_send_messages(bot, chat_id, checking)
            params['timestamp'] = checking['last_attempt_timestamp']

        return checking, params


class TgLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


if __name__ == '__main__':

    load_dotenv()
    api_token = os.environ['DEVMAN_API_TOKEN']
    bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    chat_id = os.environ['TELEGRAM_CHAT_ID']

    tg_bot = telegram.Bot(token=bot_token)

    logger.setLevel(logging.INFO)
    logger.addHandler(TgLogsHandler(tg_bot, chat_id))

    logger.info('Запущен devman_bot')

    params = {
        'timestamp': None,
    }

    while True:
        try:
            response, params = long_polling(
                api_token,
                params,
                tg_bot,
                chat_id,
                timeout=10,
            )
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            logger.exception('devman_bot')
            sleep(10)
        except Exception:
            logger.exception('devman_bot')
