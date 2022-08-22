from wtforms import StringField, SelectField, TextAreaField, DateField, validators, SubmitField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from website.extensions import * 
from website.models import *


class AddHardware(FlaskForm):
  barcode = StringField("Barcode", validators=[validators.DataRequired()])
  stanowisko = SelectField("Stanowisko", choices=[st['stanowisko'] for st in db_stanowiska.find({})], coerce=str)
  typ = SelectField("Typ", validators=[validators.DataRequired()], choices=[typ for typ in type], coerce=str)
  marka = SelectField("Marka", validators=[validators.DataRequired()], choices=[m for m in marka], coerce=str)
  model = SelectField("Model", validators=[validators.DataRequired()], choices=[mod for mod in model], coerce=str)
  stan = SelectField("Stan", validators=[validators.DataRequired()], choices=[state for state in hardware_status], coerce=str)
  bitlocker = StringField("Pin/hasło")
  serial = StringField("Nazwa/serial")
  identyfikator = StringField("Indentyfikator klucza odzyskiwania")
  klucz_odzyskiwania = StringField("Klucz/dysk odzyskiwania")
  notatki = TextAreaField("Notatki", render_kw={'rows': 4})
  mocarz_id = StringField("Moccarz ID")
  projekt = SelectField("Projekt", choices=[p for p in projekt], coerce=str)
  lokalizacja = SelectField("Lokalizacja", choices=[l for l in lokalizacja], coerce=str)


class AddHardwareFromField(FlaskForm):
  plik = FileField("Upload", validators=[validators.DataRequired()])

class AddPaperwork(FlaskForm):
  kartoteka = StringField("Kartoteka NIW", validators=[validators.DataRequired()])
  faktury = StringField("Numery faktur")
  kartoteka_typ = SelectField("Kartoteka Typ", choices=["", "Środek trwały", "Leasing"], validators=[validators.DataRequired()], coerce=str)
  mpk = SelectField("MPK", choices=[val for val in mpk], validators=[validators.DataRequired()], coerce=str)
  data_przyjecia = DateField("Data przyjęcia", format='%Y-%m-%d')

class FilterHardware(FlaskForm):
  choices_list = [state for state in hardware_status]
  choices_list.insert(0," ")
  typ = SelectField("Typ", choices=[typ for typ in type], coerce=str)
  marka = SelectField("Marka", choices=[m for m in marka], coerce=str)
  model = SelectField("Model", choices=[mod for mod in model], coerce=str)
  stan = SelectField("Stan", choices=choices_list, coerce=str)
  rented = SelectField("Wypożyczony?", choices=["","Tak", "Nie"], coerce=str)
  submit = SubmitField("Filtruj")
