import config.secrets as secrets
from pymongo import MongoClient


mongo_client = MongoClient(secrets.MONGO_URI, serverSelectionTimeoutMS=5000)
user_dbs = mongo_client['USERS']
product_dbs = mongo_client['PRODUCTS']
