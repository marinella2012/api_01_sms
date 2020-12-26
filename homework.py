import os
import time

import requests
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()


def get_status(user_id):
    vk_token = os.getenv('VK_AUTH_TOKEN')
    params = {
        'v': '5.89',
        'user_ids': user_id,
        'access_token': vk_token,
        'fields': 'online'
    }
    get_account = requests.post(
        'https://api.vk.com/method/users.get',
        params=params
        )
    status = get_account.json().get('response')[0].get('online')
    return status


def send_sms(sms_text):
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=sms_text,
        from_=os.getenv('NUMBER_FROM'),
        to=os.getenv('NUMBER_TO')
    )
    return message.sid


if __name__ == '__main__':
    vk_id = input('Введите id ')
    while True:
        if get_status(vk_id) == 1:
            send_sms(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
