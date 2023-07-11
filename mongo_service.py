from pymongo.mongo_client import MongoClient
import certifi
import constants

ca = certifi.where()

client = MongoClient(
    constants.MONGO_KEY, 
    tlsCAFile=ca
)
db = client[constants.DATABASE_NAME]
collection = db[constants.COLLECTION_NAME]

def upload_user(chat_id: int, username: str):
    filter_query = {"_id": chat_id}  
    update_query = {"username": username}
    collection.replace_one(filter_query, update_query, upsert=True)

def get_users_from_db():
    return collection.find()
