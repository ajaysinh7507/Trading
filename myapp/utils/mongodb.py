from pymongo import MongoClient

from myproject.settings import DB_HOST, DB_PASSWORD, DB_PORT, DB_USERNAME

def get_db_handle():
    client = MongoClient(host=DB_HOST, port=DB_PORT, username=DB_USERNAME, password=DB_PASSWORD)
    
    db_handle = client["djangoDemo"]
    return db_handle

def get_collection_handle(db_handle,collection_name):
    
    return db_handle[collection_name]
