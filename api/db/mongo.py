from api.settings import api_settings
from pymongo import MongoClient
import pymongo

database = MongoClient(api_settings.MONGO_URL).get_database(api_settings.DATABASE_NAME)

layer_collection = database.get_collection(api_settings.LAYER_COLLECTION)
layer_collection.create_index([("location", pymongo.GEOSPHERE)])
