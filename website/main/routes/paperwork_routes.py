from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request
from flask.json import jsonify
from website.extensions import *
from ..forms import AddPaperwork
from flask_login import login_required


paperwork = Blueprint('paperwork', __name__)


def list_to_str(list):
    str = ""
    for id, val in enumerate(list, start=1):
        if id < len(list):
            str += val.strip() + ", "
        else:
            str += val.strip()
    return str


@paperwork.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = AddPaperwork()
    free_items = db_items.find({'kartoteka': {"$exists": False}})
    if request.method == 'POST':
        faktury = form.faktury.data.split(',')
        data = {
            'przypisane_barcodes': request.form.getlist('barcodes'),
            'kartoteka': form.kartoteka.data,
            'przypisane_faktury': faktury,
            'kartoteka_typ': form.kartoteka_typ.data,
            'mpk': form.mpk.data,
            'data_faktury': form.data_przyjecia.data.strftime("%Y-%m-%d"),
            'notatki': form.notatki.data,
        }
        db_paperwork.insert_one(data)
        for each in data['przypisane_barcodes']:
            db_items.update_one({'barcode': each}, {"$set": {
                'kartoteka': form.kartoteka.data
            }})
        return redirect(url_for('main.index'))

    return render_template('add_paperwork.html', header_text="Dodaj", edit=False, form=form, available_barcodes=free_items)


@paperwork.route('/edit/<kartoteka>', methods=['GET', 'POST'])
def edit(kartoteka):
    barcodes_from_db = db_paperwork.find_one({'kartoteka': kartoteka}, {
                                             'przypisane_barcodes': 1, '_id': 0})['przypisane_barcodes']
    barcodes_to_delete = []
    form = AddPaperwork()
    free_items = db_items.find({'kartoteka': {"$exists": False}})
    # form.barcode.data = data['barcode']
    if request.method == 'POST':
        faktury = form.faktury.data.split(',')
        barcodes_from_select = request.form.getlist('barcodes')
        if len(form.barcodes_form.data) > 0:
            barcodes_from_form = form.barcodes_form.data.split(',')
        else:
            barcodes_from_form = None
        if barcodes_from_form:
            for barcode in barcodes_from_form:
                barcodes_from_select.append(barcode.strip())
        db_paperwork.update_one({'kartoteka': kartoteka}, {'$set': {
            'kartoteka': form.kartoteka.data,
            'kartoteka_typ': form.kartoteka_typ.data,
            'mpk': form.mpk.data,
            'data_faktury': form.data_przyjecia.data.strftime("%Y-%m-%d"),
            'przypisane_barcodes': barcodes_from_select,
            'przypisane_faktury': faktury,
            'notatki': form.notatki.data,
            'update_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }}, upsert=True)
        for each in barcodes_from_select:
            db_items.update_one({'barcode': each}, {"$set": {
                'kartoteka': form.kartoteka.data
            }})

        for barcode in barcodes_from_db:
            if barcode not in barcodes_from_select:
                barcodes_to_delete.append(barcode)
        if len(barcodes_to_delete) > 0:
            for barcode in barcodes_to_delete:
                db_items.update_one({'barcode': barcode}, {"$unset": {
                    'kartoteka': ""
                }})
        return (redirect(url_for('main.index')))
    else:
        rest = {}
        data = db_paperwork.find_one({'kartoteka': kartoteka}, {
                                     '_id': 0, 'update_date': 0})
        # print(data)
        # print(data.items())
        for key, value in data.items():
            if key == 'przypisane_barcodes':
                barcodes_from_db = value
                form['barcodes_form'].data = list_to_str(value)
            elif key == 'przypisane_faktury':
                form['faktury'].data = list_to_str(value)
            elif key == 'data_faktury':
                form['data_przyjecia'].data = datetime.strptime(
                    value, '%Y-%m-%d')
            else:
                rest[key] = value
        for key, value in rest.items():
            form[key].data = value
        # return render_template('add_paperwork.html',
        #                        header_text="Edytuj",
        #                        data=data,
        #                        hardware_data=False,
        #                        edit=True,
        #                        form=form)
    return render_template('add_paperwork.html', header_text="Edytuj", form=form, available_barcodes=free_items, edit=True)
    # return render_template('edit_paperwork.html', form=form, available_barcodes=free_items)


@paperwork.route('/all')
def see_all():
    all_items = db_paperwork.find({})
    return render_template('all_papers.html', items=all_items)
