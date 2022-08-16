from datetime import datetime
from genericpath import exists
from flask import Blueprint, render_template, redirect, url_for, request
from flask.json import jsonify
from website.extensions import *
from ..forms import AddHardware
from website.models import *

main = Blueprint('main', __name__)

@main.route('/')
def index():
  return render_template('index.html')

