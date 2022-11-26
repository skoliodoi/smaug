
from pymongo import MongoClient
import os

cluster = MongoClient(f"mongodb+srv://{os.environ['MONGODB_USERNAME']}:{os.environ['MONGODB_PASSWORD']}@{os.environ['MONGODB_CLUSTER']}")
db = cluster["smaug"]
db_collection = db["sm_selectables"]
db_items = db["sm_items"]
db_history = db["sm_history"]
db_stanowiska = db["sm_stanowiska"]
db_paperwork = db["sm_paperwork"]
db_users = db["sm_users"]
