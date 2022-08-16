
from pymongo import MongoClient

cluster = MongoClient('mongodb+srv://test_user:develop123@testcluster.yqbacvb.mongodb.net/?retryWrites=true&w=majority')
db = cluster["smaug"]
db_collection = db["sm_type"]
db_items = db["sm_items"]
db_history = db["sm_history"]
db_stanowiska = db["sm_stanowiska"]
db_paperwork = db["sm_paperwork"]