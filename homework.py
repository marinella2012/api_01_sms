import os
import time

import requests
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()
vk_token = os.getenv('VK_AUTH_TOKEN')
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
to = os.getenv('NUMBER_TO')
ver_api = '5.89'


def get_status(user_id):
    params = {
        'v': ver_api,
        'user_ids': user_id,
        'access_token': vk_token,
        'fields': 'online'
    }
    get_account = requests.post(
        'https://api.vk.com/method/users.get',
        params=params
        )
    try:
        get_account.raise_for_status()
    except requests.exceptions.HTTPError as error:
        print(error)
    status = get_account.json().get('response')[0].get('online')
    try:
        status.raise_for_status()
    except requests.exceptions.HTTPError as error:
        print(error)
    return status


def sms_sender(sms_text):
    from = os.getenv('NUMBER_FROM')
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=sms_text,
        from_=from,
        to=to
    )
    return message.sid


if __name__ == '__main__':
    vk_id = input('Введите id ')
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
