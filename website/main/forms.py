from wtforms import *
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from website.extensions import *
from website.dane import *


collection = db_collection.find_one({})


class Login(FlaskForm):
    email = EmailField("Email", [validators.DataRequired()])
    password = PasswordField("Hasło", [validators.DataRequired()])
    submit = SubmitField("Zaloguj się")


class Signup(FlaskForm):
    login = StringField("Login", [validators.DataRequired()])
    password = PasswordField("Hasło", [validators.DataRequired()])
    imie = StringField("Imię", [validators.DataRequired()])
    nazwisko = StringField("Nazwisko", [validators.DataRequired()])
    email = EmailField("Email", [validators.DataRequired()])
    dostep = SelectField("Typ użytkownika:", [validators.DataRequired()], choices=[
                         a for a in db_collection.find_one({})['user_type']], coerce=str)
    new_mpk = StringField("Nowy MPK", render_kw={'style': 'display: none',
                          "id": "signup-new-mpk", "placeholder": "Wpisz nowy MPK"})
    # mpk = SelectField("MPK", choices=[val for val in collection['mpk']], validators=[
    #                   validators.DataRequired()], coerce=str)
    submit = SubmitField("Zaloguj się")


class AddHardware(FlaskForm):
    barcode = StringField("Barcode", validators=[validators.DataRequired()])
    stanowisko = SelectField("Stanowisko", coerce=str, render_kw={
                             'id': 'select-stanowisko'})
    typ = SelectField("Typ sprzętu", coerce=str,
                      render_kw={'id': 'select-typ', 'required': True})
    marka = SelectField("Marka", coerce=str, render_kw={
                        'id': 'select-marka', 'required': True})
    model = SelectField("Model", coerce=str, render_kw={
                        'id': 'select-model', 'required': True})
    stan = SelectField("Stan", validators=[validators.DataRequired()], choices=[
                       state for state in collection['status']], coerce=str, render_kw={'id': 'select-stan'})
    opis_uszkodzenia = StringField("Opis uszkodzenia", render_kw={
                                   'id': 'opis-uszkodzenia-input'})
    bitlocker = StringField("Pin/hasło")
    serial = StringField("Nazwa/serial")
    identyfikator = StringField("Indentyfikator klucza odzyskiwania")
    klucz_odzyskiwania = StringField("Klucz/dysk odzyskiwania")
    notatki = TextAreaField("Notatki dot. sprzętu", render_kw={'rows': 2})

    mocarz_id = StringField("Moccarz ID")
    projekt = SelectField("Projekt", choices=[
                          p for p in collection['projekt']], coerce=str, render_kw={'id': 'select-projekt'})
    lokalizacja = SelectField("Lokalizacja", choices=[
                              l for l in collection['lokalizacja']], coerce=str, render_kw={'id': 'select-lokalizacja'})
    sluchawki = SelectField("Słuchawki", choices=[
                            "Nie dotyczy", "Axtel", "Sennheiser"], coerce=str)
    przejsciowka = SelectField("Przejściówka", choices=[
                               "Nie dotyczy", "TAK", "NIE"], coerce=str)
    zlacze = SelectField("Złącze", choices=[
                         "Nie dotyczy", "Typu USB", "Typu JACK"], coerce=str)
    mysz = SelectField(
        "Mysz", choices=["Nie dotyczy", "TAK", "NIE"], coerce=str)
    torba = SelectField(
        "Torba", choices=["Nie dotyczy", "TAK", "NIE"], coerce=str)
    modem = SelectField(
        "Modem", choices=["Nie dotyczy", "TAK", "NIE"], coerce=str)
    karta_zblizeniowa = SelectField("Karta zbliżeniowa RFID", choices=[
                                    "Nie dotyczy", "TAK", "NIE"], coerce=str)
    notatki_wypozyczenie = TextAreaField(
        "Notatki dot. wypożyczenia", render_kw={'rows': 2})

    nowy_stanowisko = StringField(
        render_kw={'style': 'display: none', 'id': 'nowy_stanowisko'})
    nowy_typ = StringField(
        render_kw={'style': 'display: none', 'id': 'nowy_typ'})
    nowa_marka = StringField(
        render_kw={'style': 'display: none', 'id': 'nowa_marka'})
    nowy_model = StringField(
        render_kw={'style': 'display: none', 'id': 'nowy_model'})
    nowy_projekt = StringField(
        render_kw={'style': 'display: none', 'id': 'nowy_projekt'})
    nowa_lokalizacja = StringField(
        render_kw={'style': 'display: none', 'id': 'nowa_lokalizacja'})


class AddHardwareFromField(FlaskForm):
    plik = FileField("Upload", validators=[validators.DataRequired()])


class ReturnHardware(FlaskForm):
    stan = SelectField("Stan", validators=[validators.DataRequired()], choices=[
                       state for state in collection['status']], coerce=str, render_kw={'id': 'zwrot-stan'})
    opis_uszkodzenia = TextAreaField("Opis uszkodzenia", render_kw={
                                     'rows': 1, 'id': 'opis-uszkodzenia'})
    dodatkowe_uwagi = TextAreaField("Dodatkowe uwagi", render_kw={
                                    'rows': 1, 'id': 'zwrot-dodatkowe-uwagi'})


class AddPaperwork(FlaskForm):
    barcodes_form = StringField("Przypisane barcode'y:")
    kartoteka = StringField("Kartoteka NIW", validators=[
                            validators.DataRequired()])
    faktury = StringField("Numery faktur")
    kartoteka_typ = SelectField("Kartoteka Typ", choices=[
                                "", "Środek trwały", "Leasing"], validators=[validators.DataRequired()], coerce=str)
    mpk = SelectField("MPK", validators=[
                      validators.DataRequired()], coerce=str,  render_kw={'placeholder': 'Wybierz MPK', 'rows': 1, 'id': 'select-mpk'})
    data_przyjecia = DateField("Data przyjęcia", format='%Y-%m-%d')
    notatki = TextAreaField("Notatki", render_kw={'rows': 4})
    nowy_mpk = StringField(
        render_kw={'style': 'display: none', 'id': 'nowy_mpk'})
# class EditPaperwork(FlaskForm):
#   kartoteka = StringField("Kartoteka NIW", validators=[validators.DataRequired()])
#   faktury = StringField("Numery faktur")
#   kartoteka_typ = SelectField("Kartoteka Typ", choices=["", "Środek trwały", "Leasing"], validators=[validators.DataRequired()], coerce=str)
#   mpk = SelectField("MPK", choices=[val for val in mpk], validators=[validators.DataRequired()], coerce=str)
#   data_przyjecia = DateField("Data przyjęcia", format='%Y-%m-%d')
#   notatki = TextAreaField("Notatki", render_kw={'rows': 4})


class FilterHardware(FlaskForm):
    choices_list = [state for state in collection['status']]
    choices_list.insert(0, " ")
    typ = SelectField(
        "Typ", choices=[typ for typ in collection['type']], coerce=str)
    marka = SelectField(
        "Marka", choices=[m for m in collection['marka']], coerce=str)
    model = SelectField(
        "Model", choices=[mod for mod in collection['model']], coerce=str)
    stan = SelectField("Stan", choices=choices_list, coerce=str)
    rented = SelectField("Wypożyczony?", choices=[
                         "", "Tak", "Nie"], coerce=str)
    submit = SubmitField("Filtruj")
