import pymongo
import constants as constants

MONGO_URL = constants.MONGODB_URI
client = pymongo.MongoClient(MONGO_URL)
database = client[constants.DATABASE]

def get_db():
    return database