from website.models import User
from ..forms import Login, Signup
from flask import Blueprint, flash, render_template, redirect, url_for, request
from website.extensions import *
from website.constants import *
from flask_login import login_user, login_required, logout_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=["POST", "GET"])
def login():
    form = Login()
    if request.method == 'POST':
        email = form.email.data
        password = form.password.data
        find_user = db_users.find_one({'email': email})
        if find_user:
            correct_pass = bcrypt.check_password_hash(
                find_user['password'], password)
        else:
            correct_pass = False
        if correct_pass:
            id = find_user['_id']
            user = User(id)
            login_user(user)
            return (redirect(url_for("main.index")))
        else:
            error_msg = ("Niepoprawny email lub hasło")
            return render_template('login.html', form=form, err=error_msg)
    else:
        return render_template('login.html', form=form)


def check_existing_users(login, email):
    existing_user = db_users.find_one(
        {"$or": [{'login': login}, {'email': email}]})
    if existing_user == None:
        return True
    else:
        return False




@auth.route('/signup', methods=["POST", "GET"])
@login_required
def signup():
    form = Signup()
    if request.method == 'POST':
        if check_existing_users(form.login.data, form.email.data):

            password = generate_pass()
            mpk_data_from_list = request.form.getlist('mpk_list')
            if form.new_mpk.data:
                new_mpk = form.new_mpk.data.split(',')
                for element in new_mpk:
                    mpk_data_from_list.append(element)
                    db_collection.update_one({"_id": "main"}, {"$addToSet": {
                                             "mpk": element}})
            # print(mpk_data_from_list)
            flash('Użytkownik dodany', category='success')
            # pw_hash = bcrypt.generate_password_hash(
            #     form.password.data).decode('utf-8')
            login = form.email.data
            email = form.email.data
            # password = form.password.data
            imie = form.imie.data
            nazwisko = form.nazwisko.data
            access = form.dostep.data
            mpk = mpk_data_from_list
            user = User.signup(login=login, email=email, password=password[0],
                               dostep=access, mpk=mpk, imie=imie, nazwisko=nazwisko)
            db_users.insert_one(user.json)
            content = f"""
        Hasło do systemu SMAUG: {password[1]}
        """
            if form.email.data != "":
                yag.send(email, "Witamy w SMAUG-u", content)
            update_for_cron("sm_users")
            return redirect(url_for('auth.signup'))
        else:
            flash('Użytkownik o podanych danych już istnieje!', category='error')
            return redirect(url_for('auth.signup'))
    else:
        collection = db_collection.find_one({})
        mpk_data = sort_and_assign(
                collection['mpk']) if check_if_exists('mpk') else []
        return render_template('signup.html', form=form, mpk_data=mpk_data, return_to="/", display_text="Dodaj")


@auth.route('/logout')
def logout():
    logout_user()
    return (redirect(url_for("auth.login")))
