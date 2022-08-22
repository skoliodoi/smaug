from datetime import datetime
from genericpath import exists
from flask import Blueprint, render_template, redirect, url_for, request
from flask.json import jsonify
from website.extensions import *
from ..forms import AddPaperwork


paperwork = Blueprint('paperwork', __name__)


@paperwork.route('/add', methods=['GET', 'POST'])
def add():
    form = AddPaperwork()
    free_items = db_items.find({'kartoteka': {"$exists": False}})
    if request.method == 'POST' and form.validate():
        faktury = form.faktury.data.split(',')
        data = {
            'przypisane_barcodes': request.form.getlist('barcodes'),
            'kartoteka': form.kartoteka.data,
            'przypisane_faktury': faktury,
            'kartoteka_typ': form.kartoteka_typ.data,
            'mpk': form.mpk.data,
            'data_faktury': form.data_przyjecia.data.strftime("%Y-%m-%d"),
            'notatki': request.form.get('notes'),
        }
        print(data)
        db_paperwork.insert_one(data)
        for each in data['przypisane_barcodes']:
            db_items.update_one({'barcode': each}, {"$set": {
                'kartoteka': form.kartoteka.data
            }})
        return redirect(url_for('main.index'))

    return render_template('add_paperwork.html', form=form, available_barcodes=free_items)


@paperwork.route('/all')
def see_all():
    all_items = db_paperwork.find({})
    return render_template('all_papers.html', items=all_items)
