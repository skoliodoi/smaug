from website.models import User
from ..forms import Login, Signup
from flask import Blueprint, flash, render_template, redirect, url_for, request
from website.extensions import *
from flask_login import login_user, login_required, logout_user
import yagmail
from flask_bcrypt import Bcrypt

yag = yagmail.SMTP(user={'njootek@gmail.com': 'SMAUG'},
                   password="uzghjsotztwpbkhe")

auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth.route('/login', methods=["POST", "GET"])
def login():
    form = Login()
    if request.method == 'POST':
        email = form.email.data
        password = form.password.data
        find_user = db_users.find_one({'email': email})
        if find_user:
          correct_pass = bcrypt.check_password_hash(find_user['password'], password)
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


@auth.route('/signup', methods=["POST", "GET"])
@login_required
def signup():

    form = Signup()
    if request.method == 'POST':
        pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        login = form.login.data
        email = form.email.data
        password = form.password.data
        imie = form.imie.data
        nazwisko = form.nazwisko.data
        access = form.access.data
        mpk = form.mpk.data
        user = User.signup(login=login, email=email, password=pw_hash,
                           dostep=access, mpk=mpk, imie=imie, nazwisko=nazwisko)
        db_users.insert_one(user.json)
        content = f"""
        Hasło do systemu SMAUG: {password}
        """
        if form.email.data != "":
          yag.send(email, "Witamy w SMAUG-u", content)
        return (redirect(url_for("main.index")))
    return render_template('signup.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return (redirect(url_for("auth.login")))