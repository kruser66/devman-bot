import os
import requests
import telegram
from time import sleep
from dotenv import load_dotenv
from pprint import pprint

def bot_send_messages(chat_id, json):

    for attempt in json['new_attempts']:
        title = 'У Вас проверили работу:\n"{}"'.format(attempt['lesson_title'])
        if attempt['is_negative']:
            correct = '_К сожалению, в работе нашлись ошибки_'
        else:
            correct = '''
            _Преподавателю все понравилось.
            Можете приступать к следующему заданию_
            '''
        link = '[Ссылка на Вашу работу]({})'.format(attempt['lesson_url'])
        try:
            bot.send_message(
                chat_id=chat_id,
                text=f'{title}\n\n{link}\n\n{correct}',
                parse_mode=telegram.ParseMode.MARKDOWN_V2
            )
        except telegram.error.TimedOut:
            print('Telegram TimeOut')


def long_polling(token):
    url = 'https://dvmn.org/api/long_polling/'

    headers = {
        'Authorization': token,
    }
    params = {
        'timestamp': '',
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    pprint(data)
    if data['status'] == 'timeout':
        params['timestamp'] = data['timestamp_to_request']
    elif data['status'] == 'found':
        bot_send_messages(tg_chat_id, data)
        params['timestamp'] = data['last_attempt_timestamp']


if __name__ == '__main__':

    load_dotenv()
    devman_api_token = os.getenv('DEVMAN_API_TOKEN')
    tg_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    tg_chat_id = os.getenv('TELEGRAM_CHAT_ID')

    bot = telegram.Bot(token=tg_bot_token)

    while True:
        try:
            long_polling(devman_api_token)

        except requests.exceptions.ReadTimeout:
            print('LongPull Timeout')
            sleep(15)
        except requests.exceptions.ConnectionError:
            print('Connection Error')
            sleep(10)
