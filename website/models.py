from flask import jsonify
from .extensions import *
from bson import ObjectId


class User():
    def __init__(self, id):
        user = db_users.find_one({'_id': ObjectId(id)})
        self.id = user['_id']
        self.imie = user['imie']
        self.dostep = user['dostep']
        self.mpk = user['mpk']
        self.login = user['login']

    def signup(**kwargs):
        user = {
            'login': kwargs['login'],
            'email': kwargs['email'],
            'password': kwargs['password'],
            'imie': kwargs['imie'],
            'nazwisko': kwargs['nazwisko'],
            'dostep': kwargs['dostep'],
        }
        if len(kwargs['mpk']) > 0:
            user['mpk'] = kwargs['mpk']
        return jsonify(user)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
