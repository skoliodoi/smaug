
from pymongo import MongoClient

cluster = MongoClient('mongodb+srv://test_user:develop123@testcluster.yqbacvb.mongodb.net/?retryWrites=true&w=majority')
db = cluster["smaug"]
collection = db["sm_type"]
items = db["sm_items"]
history = db["sm_history"]