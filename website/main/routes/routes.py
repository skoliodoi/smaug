from unicodedata import name
from flask import Blueprint, render_template, redirect, url_for, request
from website.extensions import *
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
  print(current_user)
  return render_template('main.html')

