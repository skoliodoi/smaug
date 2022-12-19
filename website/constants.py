from website.extensions import *
import pytz
from datetime import datetime
from flask_bcrypt import Bcrypt
import random
import string
import yagmail
import os


yag = yagmail.SMTP(user={f"{os.environ['MAIL_ADDRESS']}": 'SMAUG'},
                   password=f"{os.environ['MAIL_PASS']}")

local_tz = pytz.timezone('Europe/Warsaw')



user_types = ["User", "IT", "Admin"]

def list_to_str(list):
    str = ""
    for id, val in enumerate(list, start=1):
        if id < len(list):
            str += val.strip() + ", "
        else:
            str += val.strip()
    return str


def data_handler(form_data, new_data, data_name):
    returned_data = form_data
    if new_data:
        returned_data = new_data
        db_collection.update_one(
            {"_id": "main"}, {"$addToSet": {data_name: returned_data}})
    return returned_data


navbar_select_data = [('', ''), ('all', 'Wszystkie'), ('rented', 'Wypożyczone'), (
    'not-rented', 'Wolne'), ('no-barcode', 'Brak barcode\'u'), ('barcode', 'Z barcodem')]


def check_existing_data(data, data_label, database):
    database_to_check = database
    existing_record = database_to_check.find_one({data_label: data})
    if existing_record == None:
        return True
    else:
        return False

bcrypt = Bcrypt()

def generate_pass():
    characters = string.ascii_letters + string.digits + '!@#$%^&*()'
    password = ''.join(random.choice(characters) for i in range(12))
    pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    return pw_hash, password