from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash
from website.extensions import *
from ..forms import AddHardware, AddHardwareFromField, FilterHardware, ReturnHardware
from website.dane import *
import openpyxl
from flask_login import login_required, current_user

hardware = Blueprint('hardware', __name__)


def check_existing_records(barcode):

    existing_record = db_items.find_one({'barcode': barcode})
    if existing_record == None:
        return True
    else:
        return False


def go_through_file(uploaded_file):
    wb = openpyxl.load_workbook(uploaded_file)
    ws = wb.active
    hardware_rented = False
    data_table = []
    db_barcodes = []
    for row in range(2, ws.max_row+1):

        if row:
            barcode = ws.cell(row, 1).value
            if check_existing_records(barcode):
                rent_date = ws.cell(row, 14).value
                who_rented = ws.cell(row, 15).value
                if ws.cell(row, 11).value != None:
                    hardware_rented = True
                    if rent_date == None or rent_date == '':
                        rent_date = datetime.now()
                    if who_rented == None or who_rented == '':
                        who_rented = 'Osoba udostępniająca'
                data = {
                    'barcode': ws.cell(row, 1).value if ws.cell(row, 1).value != None else "N/A",
                    'stanowisko': ws.cell(row, 2).value if ws.cell(row, 2).value != None else "N/A",
                    'typ': ws.cell(row, 3).value if ws.cell(row, 3).value != None else "N/A",
                    'marka': ws.cell(row, 4).value if ws.cell(row, 4).value != None else "N/A",
                    'model': ws.cell(row, 5).value if ws.cell(row, 5).value != None else "N/A",
                    'stan': ws.cell(row, 6).value if ws.cell(row, 6).value != None else "N/A",
                    'bitlocker': ws.cell(row, 7).value if ws.cell(row, 7).value != None else "N/A",
                    'serial': ws.cell(row, 8).value if ws.cell(row, 8).value != None else "N/A",
                    'identyfikator': ws.cell(row, 9).value if ws.cell(row, 9).value != None else "N/A",
                    'klucz_odzyskiwania': ws.cell(row, 10).value if ws.cell(row, 10).value != None else "N/A",
                    'mocarz_id': ws.cell(row, 11).value if ws.cell(row, 11).value != None else "N/A",
                    'projekt': ws.cell(row, 12).value if ws.cell(row, 12).value != None else "N/A",
                    'lokalizacja': ws.cell(row, 13).value if ws.cell(row, 13).value != None else "N/A",
                    'notatki': ws.cell(row, 16).value,
                    'rented_status': hardware_rented,
                    'upload_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'rent_date': rent_date.strftime("%Y-%m-%d %H:%M:%S") if rent_date != None else rent_date,
                    'adder': 'Osoba dodająca',
                    'who_rented': who_rented
                }
                data_table.append(data)
            else:
                db_barcodes.append(barcode)
    if data_table:
        db_items.insert_many(data_table)
        db_history.insert_many(data_table)
    return db_barcodes


@hardware.route('/add_file', methods=['GET', 'POST'])
@login_required
def add_file():
    form = AddHardwareFromField()
    if request.method == 'POST':
        file = form.plik.data
        get_barcodes = go_through_file(file)
        return redirect(url_for("hardware.add_file"))
    return render_template('add_file.html', form=form)


@hardware.route('/add', methods=['GET', 'POST'])
@login_required
def add():

    hardware_form = AddHardware()

    if request.method == 'POST':
        if check_existing_records(hardware_form.barcode.data):
            typ_data = hardware_form.typ.data
            marka_data = hardware_form.marka.data
            model_data = hardware_form.model.data
            projekt_data = hardware_form.projekt.data
            lokalizacja_data = hardware_form.lokalizacja.data

            if hardware_form.typ.data == "DODAJ":
                typ_data = hardware_form.nowy_typ.data
                db_collection.update_one(
                    {"_id": "main"}, {"$addToSet": {"type": typ_data}})
            if hardware_form.marka.data == "DODAJ":
                marka_data = hardware_form.nowa_marka.data
                db_collection.update_one(
                    {"_id": "main"}, {"$addToSet": {"marka": marka_data}})
            if hardware_form.model.data == "DODAJ":
                model_data = hardware_form.nowy_model.data
                db_collection.update_one(
                    {"_id": "main"}, {"$addToSet": {"model": model_data}})
            if hardware_form.projekt.data == "DODAJ":
                projekt_data = hardware_form.nowy_projekt.data
                db_collection.update_one(
                    {"_id": "main"}, {"$addToSet": {"projekt": projekt_data}})
            if hardware_form.lokalizacja.data == "DODAJ":
                lokalizacja_data = hardware_form.nowa_lokalizacja.data
                db_collection.update_one(
                    {"_id": "main"}, {"$addToSet": {"lokalizacja": lokalizacja_data}})

            data_to_send = {
                'barcode': hardware_form.barcode.data,
                'stanowisko': hardware_form.stanowisko.data,
                'typ': typ_data,
                'marka': marka_data,
                'model': model_data,
                'stan': hardware_form.stan.data,
                'bitlocker': hardware_form.bitlocker.data,
                'serial': hardware_form.serial.data,
                'identyfikator': hardware_form.identyfikator.data,
                'klucz_odzyskiwania': hardware_form.klucz_odzyskiwania.data,
                'notatki': hardware_form.notatki.data,

                'rented_status': False,
                'upload_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                # 'rent_date': rent_date,
                'adder': current_user.login,
                # 'who_rented': who_rented
            }
            if hardware_form.mocarz_id.data != None and hardware_form.mocarz_id.data != "":
                try:
                    data_to_send['rented_status'] = True
                    data_to_send['mocarz_id'] = hardware_form.mocarz_id.data
                    data_to_send['projekt'] = projekt_data
                    data_to_send['lokalizacja'] = lokalizacja_data
                    data_to_send['karta_zblizeniowa'] = hardware_form.karta_zblizeniowa.data
                    data_to_send['sluchawki'] = hardware_form.sluchawki.data
                    data_to_send['zlacze'] = hardware_form.zlacze.data
                    data_to_send['przejsciowka'] = hardware_form.przejsciowka.data
                    data_to_send['mysz'] = hardware_form.mysz.data
                    data_to_send['torba'] = hardware_form.torba.data
                    data_to_send['modem'] = hardware_form.modem.data
                    data_to_send['notatki_wypozyczenie'] = hardware_form.notatki_wypozyczenie.data
                    data_to_send['who_rented'] = current_user.login
                    data_to_send['rent_date'] = datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S")

                except Exception as e:
                    print(e)
            db_history.insert_one(data_to_send)
            db_items.insert_one(data_to_send)
            if hardware_form.stanowisko.data != '':
                db_stanowiska.update_one({'stanowisko': hardware_form.stanowisko.data}, {"$push": {
                    'assigned_barcodes': hardware_form.barcode.data,
                },
                }, upsert=True)

            return (redirect(url_for('hardware.add')))
        else:
            flash('Taki sprzęt już istnieje', category='error')
            return render_template('add_items.html',
                           header_text="Dodaj",
                           form=hardware_form,
                           edit=False,
                           hardware_data=False,
                           show_rent_hardware=False)
    else:
        collection = db_collection.find_one({})
        hardware_form.typ.choices = collection['type']
        hardware_form.marka.choices = collection['marka']
        hardware_form.model.choices = collection['model']
        hardware_form.projekt.choices = collection['projekt']
        hardware_form.lokalizacja.choices = collection['lokalizacja']

    return render_template('add_items.html',
                           header_text="Dodaj",
                           form=hardware_form,
                           edit=False,
                           hardware_data=False,
                           show_rent_hardware=False)


@hardware.route('/edit/<barcode>', methods=['GET', 'POST'])
@login_required
def edit(barcode):
    form = AddHardware()

    # form.barcode.data = data['barcode']

    if request.method == 'POST':
        db_items.update_one({'barcode': barcode}, {'$set': {
            'barcode': form.barcode.data,
            'stanowisko': form.stanowisko.data,
            'typ': form.typ.data,
            'marka': form.marka.data,
            'model': form.model.data,
            'stan': form.stan.data,
            'bitlocker': form.bitlocker.data,
            'serial': form.serial.data,
            'identyfikator': form.identyfikator.data,
            'klucz_odzyskiwania': form.klucz_odzyskiwania.data,
            'notatki': form.notatki.data
        }}, upsert=True)
        return (redirect(url_for('main.index')))
    else:
        data = db_items.find_one({'barcode': barcode}, {'_id': 0,
                                                        'rented_status': 0,
                                                        'upload_date': 0,
                                                        'last_updated': 0,
                                                        'rent_date': 0,
                                                        'adder': 0,
                                                        'who_rented': 0,
                                                        'kartoteka': 0,
                                                        'bitlocker1': 0,
                                                        'bitlocker2': 0,
                                                        'mpk': 0,
                                                        'notes': 0})
        for key, value in data.items():
            form[key].data = value
        return render_template('add_items.html',
                               header_text="Edytuj",
                               data=data,
                               hardware_data=False,
                               edit=True,
                               form=form)


@hardware.route('/get_data')
@login_required
def get_data():
    form = AddHardware()
    data = form.typ.data
    print(data)
    free_items = db_items.find({'rented_status': False})
    return render_template('all_items.html', items=free_items)


@hardware.route('/rent/<barcode>', methods=['GET', 'POST'])
@login_required
def rent(barcode):
    hardware_form = AddHardware()
    hardware_data = db_items.find_one({'barcode': barcode})
    if request.method == 'POST':
        db_items.update_one({'barcode': barcode}, {"$set": {
            'mocarz_id': hardware_form.mocarz_id.data,
            'projekt': hardware_form.projekt.data,
            'lokalizacja': hardware_form.lokalizacja.data,
            'karta_zblizeniowa': hardware_form.karta_zblizeniowa.data,
            'sluchawki': hardware_form.sluchawki.data,
            'zlacze': hardware_form.zlacze.data,
            'przejsciowka': hardware_form.przejsciowka.data,
            'mysz': hardware_form.mysz.data,
            'torba': hardware_form.torba.data,
            'modem': hardware_form.modem.data,
            'notatki_wypozyczenie': hardware_form.notatki_wypozyczenie.data,
            'rented_status': True,
            'rent_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'who_rented': current_user.login
        }
        }
        )
        db_history.update_one({'barcode': barcode, 'returned': {"$exists": False}}, {"$set": {
            'mocarz_id': hardware_form.mocarz_id.data,
            'projekt': hardware_form.projekt.data,
            'lokalizacja': hardware_form.lokalizacja.data,
            'karta_zblizeniowa': hardware_form.karta_zblizeniowa.data,
            'sluchawki': hardware_form.sluchawki.data,
            'zlacze': hardware_form.zlacze.data,
            'przejsciowka': hardware_form.przejsciowka.data,
            'mysz': hardware_form.mysz.data,
            'torba': hardware_form.torba.data,
            'modem': hardware_form.modem.data,
            'notatki_wypozyczenie': hardware_form.notatki_wypozyczenie.data,
            'rented_status': True,
            'rent_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'who_rented': current_user.login
        }
        }, upsert=True
        )
        return (redirect(url_for('hardware.see_all')))
    hardware_form.notatki.data = hardware_data['notatki']

    return render_template('add_items.html',
                           udostepnienie=True,
                           header_text="Udostępnij",
                           hardware_data=hardware_data,
                           form=hardware_form)


@hardware.route('/see_history/<barcode>')
@login_required
def see_history(barcode):
    hardware_data_history = db_history.find({'barcode': barcode})
    creation_date = hardware_data_history[0]['upload_date']
    creator = hardware_data_history[0]['adder']
    return render_template("hardware_history.html", creator=creator, barcode=barcode, date=creation_date, history=hardware_data_history)


@hardware.route('/return/<barcode>', methods=['GET', 'POST'])
@login_required
def return_hardware(barcode):
    form = ReturnHardware()
    hardware_data = db_items.find_one({'barcode': barcode})
    if request.method == "POST":
        stan = form.stan.data
        opis_szkod = form.opis_uszkodzenia.data
        dodatkowe_uwagi = form.dodatkowe_uwagi.data
        db_history.update_one({'barcode': barcode, 'rent_date': hardware_data['rent_date']}, {"$set": {
            'rented_status': False,
            'returned': True,
            'return_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'who_accepted_return': current_user.login
        }})

        db_items.update_one({'barcode': barcode}, {
            "$set": {
                'rented_status': False,
                'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'stan': stan
            },
            "$unset": {
                'mocarz_id': "",
                'projekt': "",
                'lokalizacja': "",
                'rent_date': "",
                'who_rented': "",
                'notatki_wypozyczenie': "",
                'karta_zblizeniowa': "",
                'sluchawki': "",
                'zlacze': "",
                'przejsciowka': "",
                'mysz': "",
                'torba': "",
                'modem': "",
            }
        }
        )

        if opis_szkod:
            db_items.update_one({'barcode': barcode}, {
                "$set": {
                    'opis_szkod': opis_szkod
                }})

        return (redirect(url_for('hardware.see_all')))
    else:
        return render_template("return_hardware.html", hardware_data=hardware_data, paperwork_data=None, being_returned=True, form=form)


@ hardware.route('/show_info/<barcode>')
@ login_required
def show_info(barcode):
    hardware_data = db_items.find_one({'barcode': barcode})
    check_kartoteka = db_items.find_one(
        {"$and": [{'barcode': barcode}, {'kartoteka': {"$exists": True}}]})
    if check_kartoteka == None:
        paperwork_data = None
    else:
        paperwork_data = db_paperwork.find_one(
            {'kartoteka': check_kartoteka['kartoteka']})
        print(paperwork_data)
    return render_template("information_page.html", hardware_data=hardware_data, paperwork_data=paperwork_data)


@ hardware.route('/details')
@ login_required
def details():
    return render_template('hardware_details.html')


@ hardware.route('/all', methods=["GET", "POST"])
@ login_required
def see_all():
    form = FilterHardware()
    # data = {
    #     'typ': form.typ.data
    #   }
    # print(data)

    if request.method == 'POST':
        return redirect(url_for('main.index'))
    else:
        all_items = db_items.find({})
        return render_template('all_items.html', items=all_items, form=form)
