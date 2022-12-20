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


# if hardware_form.nowy_mpk.data:
#     mpk_data['data'] = hardware_form.nowy_mpk.data
#     db_collection.update_one(
#         {"_id": "main"}, {"$addToSet": {"mpk": {"nazwa": mpk_data['data'], "last_update": local_time}}})
# mpk_data = data_handler(form.mpk.data, form.nowy_mpk.data, "mpk")


def data_handler(form_data, new_data, data_name):
    local_time = datetime.now(
        local_tz).strftime("%Y-%m-%d %H:%M:%S")
    returned_data = {
        'nazwa': data_name,
        'data': form_data
    }
    if form_data or new_data:
      if new_data:
          returned_data['data'] = new_data
          existing_data = db_collection.find_one(
              {'_id': 'main', data_name: {"$elemMatch": {'nazwa': returned_data['data']}}}, {
                  data_name: 1
              })
          if existing_data:
              db_collection.update_one({f"{data_name}.nazwa": returned_data['data']}, {
                  "$set": {f"{data_name}.$.last_update": local_time}})
          else:
              db_collection.update_one(
                  {"_id": "main"}, {"$addToSet": {data_name: {"nazwa": returned_data['data'], "last_update": local_time}}})
      else:
          db_collection.update_one({f"{data_name}.nazwa": returned_data['data']}, {
              "$set": {f"{data_name}.$.last_update": local_time}})
    return returned_data['data']
# def data_handler(form_data, new_data, data_name):
#     returned_data = form_data
#     if new_data:
#         returned_data = new_data
#         db_collection.update_one(
#             {"_id": "main"}, {"$addToSet": {data_name: returned_data}})
#     return returned_data


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


def sort_and_assign(collection, mandatory=True):
    if collection and len(collection) > 0:
        sorted_table = [each['nazwa'] for each in sorted(
            collection, key=lambda d:d['last_update'], reverse=True)]
        if not mandatory:
            sorted_table.insert(0, "")
        return sorted_table
    else:
        return []


def check_if_exists(value):
    existing_value = db_collection.find_one(
        {"_id": "main", value: {"$exists": True}})
    if existing_value:
        # sorted_value = sort_and_assign(collection[value], bool)
        return True
    else:
        return False
