from myapp.Utils.mongodb import get_db_handle, get_collection_handle
from myapp.Utils.ValidateDBData import ValidateDBData
class User:
    
    def __init__(self):
        self.db_handle = get_db_handle()
        self.user = get_collection_handle(self.db_handle, "users")
        self.schema = {
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

    def create(self, data):
        try:
            validate_res = ValidateDBData(self.schema, data)

            if not validate_res["status"]:
                return validate_res

            User = self.user
            result = User.insert_one(data)

            return {"status": True, "result": result}
        except Exception as e:
            print(e)
            return {"status": False, "error": e}   

            