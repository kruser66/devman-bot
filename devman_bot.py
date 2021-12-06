import os
import requests
from time import sleep
from dotenv import load_dotenv
from pprint import pprint


def fetch_user_reviews(token):
    url = 'https://dvmn.org/api/user_reviews/'

    headers = {
        'Authorization': token,
    }

    response = requests.get(url, headers=headers)

    if response.ok:
        return response.json()


def fetch_long_pulling(token):
    url = 'https://dvmn.org/api/long_polling/'

    headers = {
        'Authorization': token,
    }

    params = {
        'timestamp': '',
    }
    while True:
        try:
            response = requests.get(url, headers=headers, params=params)
            answer = response.json()
            pprint(answer)
            if answer['status'] == 'timeout':
                params['timestamp'] = answer['timestamp_to_request']
        
        except requests.exceptions.ReadTimeout:
            print('LongPull Timeout')
            sleep(15)

        except requests.exceptions.ConnectionError:
            print('Connection Error')
            sleep(60)
  

if __name__ == '__main__':

    load_dotenv()
    token = os.getenv('DEVMAN_API_TOKEN')

    # pprint(fetch_user_reviews(token))
    fetch_long_pulling(token)