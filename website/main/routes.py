from flask import Blueprint, render_template, redirect, url_for, request
from website.extensions import collection

# todo_collection = mongo.db["smaug"]

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/add_todo', methods=['POST'])
def add_todo():
    todo_item = request.form.get('add-todo')
    collection.insert_one({'text': todo_item, 'complete': False})
    return (redirect(url_for('main.index')))
