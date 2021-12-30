from myapp.Utils.mongodb import get_db_handle, get_collection_handle
from myapp.Utils.ValidateDBData import ValidateDBData

class Script:
    
    def __init__(self):
        self.db_handle = get_db_handle()
        self.script = get_collection_handle(self.db_handle, "script")
        self.schema = {
                        "instrument_token": "int",
                        "exchange_token": "int",
                        "tradingsymbol": "str",
                        "name": "str",
                        "last_price": "float",
                        "expiry": "str",
                        "strike": "float",
                        "tick_size": "float",
                        "lot_size": "int",
                        "instrument_type": "str",
                        "segment": "str",
                        "exchange": "str",
                        "date": "str",
                        "status": "bool",
                    }
    
    def getOne(self, query={}):
        try:
            Script = self.script
            result = Script.find_one(query)

            return {"status": True, "result": result}
        except Exception as e:
            print(e)
            return {"status": False, "error": e}
    
    def getAll(self, query={}, sort={}):
        try:
            Script = self.script
            result = list(Script.find(query))
            
            return {"status": True, "result": result}
        except Exception as e:
            print(e)
            return {"status": False, "error": e}

    def create(self, data):
        try:
            validate_res = ValidateDBData(self.schema, data)

            if not validate_res["status"]:
                return validate_res

            Script = self.script
            result = Script.insert_one(data)

            return {"status": True, "result": result}
        except Exception as e:
            print(e)
            return {"status": False, "error": e}   

            