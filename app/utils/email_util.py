import requests
from rest_framework.utils import json

API_KEY = 'dqi9mkcj7ged9b9x951ea42yh1f'


def send_order_email(data):
    dump_data = json.dumps(data)
    print(dump_data)
    params = {
        'API_KEY': API_KEY
    }
    try:
        r = requests.post('https://yshuynh2.pythonanywhere.com/send_order_email', data={'dump_data':dump_data}, timeout=0.1, params=params)
        # r = requests.post('http://localhost:1234/send_order_email', data={'dump_data':dump_data}, timeout=0.1, params=params)
    except Exception as e:
        print(str(e))
    return True


def send_register_email(data):
    dump_data = json.dumps(data)
    print(dump_data)
    params = {
        'API_KEY': API_KEY
    }
    try:
        r = requests.post('https://yshuynh2.pythonanywhere.com/send_register_email', data={'dump_data':dump_data}, timeout=0.1, params=params)
        # r = requests.post('http://localhost:1234/send_register_email', data={'dump_data':dump_data}, timeout=0.1, params=params)
    except Exception as e:
        print(str(e))
    return True
