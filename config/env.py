from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db_name = "gestion_hospitalaria"
db = client[db_name]