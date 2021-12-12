import os
import requests
import telegram
from time import sleep
from dotenv import load_dotenv
from pprint import pprint

def bot_send_messages(bot, chat_id, server_answer):

    for attempt in server_answer['new_attempts']:
        title = 'У Вас проверили работу:\n"{}"'.format(attempt['lesson_title'])
        if attempt['is_negative']:
            correct = '_К сожалению, в работе нашлись ошибки_'
        else:
            correct = '''
            _Преподавателю все понравилось.
            Можете приступать к следующему заданию_
            '''
        link = '[Ссылка на Вашу работу]({})'.format(attempt['lesson_url'])
        bot.send_message(
            chat_id=chat_id,
            text=f'{title}\n\n{link}\n\n{correct}',
            parse_mode=telegram.ParseMode.MARKDOWN_V2
        )


def long_polling(token, bot, chat_id, timeout=90):
    api_url = 'https://dvmn.org/api/long_polling/'

    headers = {
        'Authorization': token,
    }
    params = {
        'timestamp': None,
    }

    while True:
        response = requests.get(
            api_url,
            headers=headers,
            params=params,
            timeout=timeout
        )
        response.raise_for_status()

        server_answer = response.json()

        if server_answer['status'] == 'timeout':
            params['timestamp'] = server_answer['timestamp_to_request']
        elif server_answer['status'] == 'found':
            bot_send_messages(bot, chat_id, server_answer)
            params['timestamp'] = server_answer['last_attempt_timestamp']


if __name__ == '__main__':

    load_dotenv()
    api_token = os.getenv('DEVMAN_API_TOKEN')
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')

    bot = telegram.Bot(token=bot_token)

    while True:
        try:
            response = long_polling(api_token, bot, chat_id, timeout=10)
            pprint(response)
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            print('Connection Error')
            sleep(10)
        except telegram.error.TimedOut:
            print('Telegram TimeOut')
