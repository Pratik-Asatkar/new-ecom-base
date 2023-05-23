from uuid import uuid4
from time import time
from datetime import datetime

def current_epoch():
    return int(time())


def current_time():
    return datetime.now().strftime("%d-%m-%Y %H:%M")


def get_cart_id():
    return str(uuid4()).split('-')[0]
