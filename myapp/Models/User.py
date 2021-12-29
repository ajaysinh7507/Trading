from logging import error
from bson import ObjectId
from myapp.Utils.mongodb import get_db_handle, get_collection_handle
class User:
    
    def __init__(self):
        db_handle = get_db_handle()
        self.user = get_collection_handle(db_handle, "users")

    def schema(self):
        schema = {
            "firstName": "str",
            "lastName": "str",
            "mobileNo": "str",
            "email": "str",
            "status": "bool",
            "date": "str"
        }
    
    def getOne(self, query={}):
        try:
            User = self.user
            result = User.find_one(query)

            return {"status": True, "result": result}
        except Exception as e:
            print(e)
            return {"status": False, "error": e}
    
    def getAll(self, query={}, sort={}):
        try:
            User = self.user
            result = User.find(query).sort(sort)

            return {"status": True, "result": result}
        except Exception as e:
            print(e)
            return {"status": False, "error": e}