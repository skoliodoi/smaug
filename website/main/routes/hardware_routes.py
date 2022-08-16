from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request
from website.extensions import *
from ..forms import AddHardware
from website.models import *

hardware = Blueprint('hardware', __name__)


@hardware.route('/add', methods=['GET', 'POST'])
def add():
    hardware_form = AddHardware()

    if request.method == 'POST':
        hardware_rented = False
        who_rented = ''
        rent_date = ''
        if hardware_form.mocarz_id.data != None and hardware_form.mocarz_id.data != "":
            hardware_rented = True
            who_rented = 'Osoba udostępniająca'
            rent_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_to_send = {
            'barcode': hardware_form.barcode.data,
            'stanowisko': hardware_form.stanowisko.data,
            'typ': hardware_form.typ.data,
            'marka': hardware_form.marka.data,
            'model': hardware_form.model.data,
            'stan': hardware_form.stan.data,
            'bitlocker': hardware_form.bitlocker.data,
            'serial': hardware_form.serial.data,
            'identyfikator': hardware_form.identyfikator.data,
            'klucz_odzyskiwania': hardware_form.klucz_odzyskiwania.data,
            'mocarz_id': hardware_form.mocarz_id.data,
            'projekt': hardware_form.projekt.data,
            'lokalizacja': hardware_form.lokalizacja.data,
            'notatki': hardware_form.notatki.data,
            'rented_status': hardware_rented,
            'upload_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'rent_date': rent_date,
            'adder': 'Osoba dodająca',
            'who_rented': who_rented
        }
        db_history.insert_one(data_to_send)
        db_items.insert_one(data_to_send)
        if hardware_form.stanowisko.data != '':
            db_stanowiska.update_one({'stanowisko': hardware_form.stanowisko.data}, {"$push": {
                'assigned_barcodes': hardware_form.barcode.data,
            },
            }, upsert=True)
        return (redirect(url_for('main.index')))
    else:
        pass
    return render_template('add_items.html', form=hardware_form, hardware_data=False, show_rent_hardware=False)


@hardware.route('/show_rent', methods=['POST'])
def show_rent():
    req_data = request.get_json()
    print(req_data)
    return (redirect(url_for('main.index'), show_rent_hardware=False))


@hardware.route('/get_data')
def get_data():
    free_items = db_items.find({'rented_status': "Nieudostępniony"})
    return render_template('all_items.html', items=free_items)


@hardware.route('/rent/<barcode>', methods=['GET', 'POST'])
def rent(barcode):
    hardware_form = AddHardware()
    hardware_data = db_items.find_one({'barcode': barcode})
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
        db_history.insert_one(
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
        db_items.update_one({'barcode': barcode}, {"$set": {
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

    return render_template('add_items.html', hardware_data=hardware_data, form=hardware_form)


@hardware.route('/see_history/<barcode>')
def see_history(barcode):
    hardware_data_history = db_history.find({'barcode': barcode})
    creation_date = hardware_data_history[0]['upload_date']
    creator = hardware_data_history[0]['adder']
    return render_template("hardware_history.html", creator=creator, barcode=barcode, date=creation_date, history=hardware_data_history)


@hardware.route('/return/<barcode>', methods=['GET', 'POST'])
def return_hardware(barcode):
    hardware_data = db_items.find_one({'barcode': barcode})

    db_history.update_one({'barcode': barcode, 'rent_date': hardware_data['rent_date']}, {"$set": {
        'rented_status': 'Zwrócony',
        'return_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'who_accepted_return': 'Osoba przyjmująca zwrot'
    }})

    db_items.update_one({'barcode': barcode}, {"$set": {
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


@hardware.route('/show_info/<barcode>')
def show_info(barcode):
    hardware_data = db_items.find_one({'barcode': barcode})
    return render_template("information_page.html", hardware_data=hardware_data)


@hardware.route('/details')
def details():
    return render_template('hardware_details.html')


@hardware.route('/all')
def see_all():
    all_items = db_items.find({})
    return render_template('all_items.html', items=all_items)
