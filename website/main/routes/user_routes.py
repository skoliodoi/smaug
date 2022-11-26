from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from website.extensions import *
from website.constants import *
from bson import ObjectId
from .auth import generate_pass, yag
from ..forms import Signup


users = Blueprint('users', __name__)

# navbar_select_data = [('', ''), ('all', 'Wszystkich'), ('rented', 'Wypożyczone'), (
#     'not-rented', 'Wolne'), ('no-barcode', 'Brak barcode\'u'), ('barcode', 'Z barcodem')]


@users.route('/all', methods=["POST", "GET"])
@login_required
def all_users():
    if request.method == 'POST':
        return redirect(url_for('main.index'))
    else:
        user_list = []
        all_users = db_users.find(
            {"login": {"$ne": current_user.login}}, {'password': 0})
        for each in all_users:
            user_list.append(each)
        return render_template('all_users.html', users=user_list)


@users.route('/reset_pass/<id>', methods=["POST", "GET"])
@login_required
def reset_pass(id):
  if request.method == 'POST':
    user = db_users.find_one({'_id': ObjectId(id)})
    user_mail = user['email']
    password = generate_pass()
    content = f"""
    Dostaliśmy prośbę o zresetowanie hasła do konta <b>{user['email']}</b>.
    Nowe hasło do systemu SMAUG: <b>{password[1]}</b> <br>
    Jeśli ten mail nie dotyczy Ciebie, zignoruj go.
    """
    yag.send(user_mail, "Nowe hasło do systemu SMAUG", content)
    db_users.update_one({"_id": ObjectId(id)}, {
                        "$set": {"password": password[0]}})
    flash(f"Hasło dla {user_mail} zostało zresetowane", "success")
    return redirect(url_for('users.all_users'))
  else:
    return render_template("confirmation.html", id=id, return_to="/users/all")


@users.route('/edit/<id>', methods=["POST", "GET"])
@login_required
def edit_user(id):
    form = Signup()
    assigned_mpk = []
    user = db_users.find_one({'_id': ObjectId(id)}, {'password': 0, '_id': 0})
    existing_mpk = db_users.find_one(
        {'mpk': {"$exists": True}, '_id': ObjectId(id)})
    if request.method == 'POST':
        try:
            db_users.update_one({'_id': ObjectId(id)}, {
                '$set': {
                    "login": form.login.data,
                    "email": form.email.data,
                    "imie": form.imie.data,
                    "nazwisko": form.nazwisko.data,
                    "dostep": form.dostep.data,
                }}, upsert=True)

            if form.dostep.data == user_types[0]:
                mpk_data_from_list = request.form.getlist('mpk_list')
                if form.new_mpk.data:
                    new_mpk = form.new_mpk.data.split(',')
                    for element in new_mpk:
                        mpk_data_from_list.append(element)
                        db_collection.update_one({"_id": "main"}, {"$addToSet": {
                            "mpk": element}}, upsert=True)

                if not existing_mpk:
                    db_users.update_one({"_id": ObjectId(id)}, {
                        "$set": {"mpk": mpk_data_from_list}})
                else:
                    for mpk in mpk_data_from_list:
                        db_users.update_one({"_id": ObjectId(id)}, {"$addToSet": {
                            "mpk": mpk}}, upsert=True)
                    mpk_from_db = user['mpk']
                    for db_mpk in mpk_from_db:
                        if db_mpk not in mpk_data_from_list:
                            db_users.update_one({"_id": ObjectId(id)}, {
                                "$pull": {"mpk": db_mpk}})
            else:
                db_users.update_one({"_id": ObjectId(id)}, {
                                    "$unset": {"mpk": ""}}, upsert=True)
            flash(
                f"Użytkownik {user['login']} został zaktualizowany", "success")
            return redirect(url_for('users.all_users'))
        except Exception as e:
            print(e)
            flash(f"{e}", "error")
            return redirect(url_for('users.all_users'))
    else:
        collection = db_collection.find_one({})
        mpk_data = collection['mpk']
        form.login.data = user['login']
        form.email.data = user['email']
        form.imie.data = user['imie']
        form.nazwisko.data = user['nazwisko']
        form.dostep.data = user['dostep']

        existing_mpk = db_users.find_one(
            {'mpk': {"$exists": True}, '_id': ObjectId(id)})
        if existing_mpk:
            print('yeah')
            for each in mpk_data:
                if each in user['mpk']:
                    assigned_mpk.append({'mpk': each, 'selected': True})
                else:
                    assigned_mpk.append({'mpk': each, 'selected': False})
            print(assigned_mpk)
            mpk_data = assigned_mpk
            edit_for_user = True
        else:
            edit_for_user = False

    return render_template('signup.html', form=form, mpk_data=mpk_data, edit=edit_for_user, display_text="Edytuj")


@users.route('/delete/<id>', methods=["POST", "GET"])
@login_required
def delete_user(id):
    if request.method == 'POST':
      db_users.delete_one({'_id': ObjectId(id)})
      flash(f"Użytkownik został usunięty", "success")
      return redirect(url_for('users.all_users'))
    else: 
      return render_template("confirmation.html", id=id, return_to="/users/all")
