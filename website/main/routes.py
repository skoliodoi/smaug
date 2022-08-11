from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request
from flask.json import jsonify
from website.extensions import *
from website.models import *

# todo_collection = mongo.db["smaug"]

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        hardware_rented = 'Nieudostępniony'
        who_rented = ''
        rent_date = ''
        if request.form.get('mocarz-id') != None and request.form.get('mocarz-id') != "":
            hardware_rented = 'Udostępniony'
            who_rented = 'Osoba udostępniająca'
            rent_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_to_send = {
            'barcode': request.form.get('barcode'),
            'type': request.form.get('type'),
            'mark': request.form.get('marka'),
            'model': request.form.get('model'),
            'status': request.form.get('status'),
            'bitlocker': request.form.get('bitlocker'),
            'serial': request.form.get('serial'),
            'identyfikator': request.form.get('identyfikator'),
            'klucz_odzyskiwana': request.form.get('klucz-odzyskiwania'),
            'mocarz_id': request.form.get('mocarz-id'),
            'projekt': request.form.get('projekt'),
            'lokalizacja': request.form.get('lokalizacja'),
            'mpk': request.form.get('mpk'),
            'notes': request.form.get('notes'),
            'rented_status': hardware_rented,
            'upload_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'rent_date': rent_date,
            'adder': 'Osoba dodająca',
            'who_rented': who_rented
        }
        history.insert_one(data_to_send)
        items.insert_one(data_to_send)
        return (redirect(url_for('main.index')))
    else:
        pass
    return render_template('add_items.html',
                           hardware_data=False,
                           type_list=type,
                           mark_list=marka,
                           model_list=model,
                           status_list=hardware_status,
                           projekt=projekt,
                           lokalizacja=lokalizacja)


@main.route('/get_data')
def get_data():
    free_items = items.find({'rented_status': "Nieudostępniony"})
    return render_template('all_items.html', items=free_items)


@main.route('/paperwork', methods=['GET', 'POST'])
def paperwork():
    free_items = items.find({'rented_status': "Nieudostępniony"})
    if request.method == 'POST':
        barcodes = request.form.getlist('barcodes')
        print(barcodes)
        return redirect(url_for('main.paperwork'))

    return render_template('add_paperwork.html', kartoteka=kartoteka, mpk_list=mpk, available_barcodes=free_items)


@main.route('/rent_hardware/<barcode>', methods=['GET', 'POST'])
def rent_hardware(barcode):
    hardware_data = items.find_one({'barcode': barcode})
    if request.method == 'POST':
        mocarz_id = request.form.get('mocarz')
        send_projekt = request.form.get('projekt')
        send_lokalizacja = request.form.get('lokalizacja')
        send_mpk = request.form.get('mpk')
        bitlocker1 = request.form.get('bitlocker-1')
        bitlocker2 = request.form.get('bitlocker-2')
        send_notes = request.form.get('notes')
        # upload_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        # adder = 'Test'
        history.insert_one(
            {
                'barcode': barcode,
                'type': hardware_data['type'],
                'mark': hardware_data['mark'],
                'model': hardware_data['model'],
                'serial': hardware_data['serial'],
                'kartoteka': hardware_data['kartoteka'],
                'mocarz_id': mocarz_id,
                'projekt': send_projekt,
                'lokalizacja': send_lokalizacja,
                'mpk': send_mpk,
                'bitlocker1': bitlocker1,
                'bitlocker2': bitlocker2,
                'notes': send_notes,
                'rented_status': 'Udostępniony',
                'rent_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'who_rented': 'Osoba udostępniająca'
            }
        )
        items.update_one({'barcode': barcode}, {"$set": {
            'mocarz_id': mocarz_id,
            'projekt': send_projekt,
            'lokalizacja': send_lokalizacja,
            'mpk': send_mpk,
            'bitlocker1': bitlocker1,
            'bitlocker2': bitlocker2,
            'notes': send_notes,
            'rented_status': 'Udostępniony',
            'rent_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'who_rented': 'Osoba udostępniająca'
        }
        }
        )
        return (redirect(url_for('main.index')))

    return render_template('add_items.html', hardware_data=hardware_data, type_list=type, mark_list=marka, model_list=model, mpk_list=mpk, kartoteka=kartoteka, projekt=projekt, lokalizacja=lokalizacja)


@main.route('/see_history/<barcode>')
def see_history(barcode):
    hardware_data_history = history.find({'barcode': barcode})
    creation_date = hardware_data_history[0]['upload_date']
    creator = hardware_data_history[0]['adder']
    return render_template("hardware_history.html", creator=creator, barcode=barcode, date=creation_date, history=hardware_data_history)


@main.route('/return_hardware/<barcode>', methods=['GET', 'POST'])
def return_hardware(barcode):
    hardware_data = items.find_one({'barcode': barcode})

    history.update_one({'barcode': barcode, 'rent_date': hardware_data['rent_date']}, {"$set": {
        'rented_status': 'Zwrócony',
        'return_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'who_accepted_return': 'Osoba przyjmująca zwrot'
    }})

    # history.insert_one(
    #     {
    #         'barcode': barcode,
    #         'type': hardware_data['type'],
    #         'mark': hardware_data['mark'],
    #         'model': hardware_data['model'],
    #         'serial': hardware_data['serial'],
    #         'kartoteka': hardware_data['kartoteka'],
    #         'mocarz_id': hardware_data['mocarz_id'],
    #         'projekt': hardware_data['projekt'],
    #         'lokalizacja': hardware_data['lokalizacja'],
    #         'mpk': hardware_data['mpk'],
    #         'bitlocker1': hardware_data['bitlocker1'],
    #         'bitlocker2': hardware_data['bitlocker2'],
    #         'notes': hardware_data['notes'],
    #         'rented_status': 'Zwrócony',
    #         'rent_date': hardware_data['rent_date'],
    #         'return_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #         'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #         'who_accepted_return': 'Osoba przyjmująca zwrot'
    #     }
    # )
    items.update_one({'barcode': barcode}, {"$set": {
        'mocarz_id': "",
        'projekt': "",
        'lokalizacja': "",
        'mpk': "",
        'bitlocker1': "",
        'bitlocker2': "",
        'notes': "",
        'rented_status': 'Nieudostępniony',
        'rent_date': "",
        'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'who_rented': ''
    }
    }
    )
    return (redirect(url_for('main.index')))


@main.route('/information_page/<barcode>')
def show_info(barcode):
    hardware_data = items.find_one({'barcode': barcode})
    return render_template("information_page.html", hardware_data=hardware_data)


@main.route('/hardware_details')
def show_hardware():
    return render_template('hardware_details.html')


@main.route('/all')
def see_all():
    all_items = items.find({})
    return render_template('all_items.html', items=all_items)
