
from pymongo import MongoClient

cluster = MongoClient('mongodb+srv://Szymon:P4cz4ng4!@testcluster.yqbacvb.mongodb.net/?retryWrites=true&w=majority')
db = cluster["smaug"]
collection = db["sm_type"]