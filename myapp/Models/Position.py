import pandas as pd
from myapp.Utils.mongodb import get_db_handle, get_collection_handle
from myapp.Utils.ValidateDBData import ValidateDBData

class Position:
    
    def __init__(self):
        self.db_handle = get_db_handle()
        self.position = get_collection_handle(self.db_handle, "position")
        self.schema = {
                        "nfo_details": "str", 
                        "trading_symbol": "str", 
                        "instrument_token": "str", 
                        "down_step": "str", 
                        "Position_id1": "str", 
                        "option_type": "str", 
                        "transaction_type": "str", 
                        "quantity": "int",  
                        "trade_time1": "str", 
                        "trade_date1": "str", 
                        "status": "bool"
                    }
    
    def getOne(self, query={}):
        try:
            Position = self.position
            result = Position.find_one(query)

            return {"status": True, "result": result}
        except Exception as e:
            print(e)
            return {"status": False, "error": e}
    
    def getAll(self, query={}, sort={}):
        try:
            Position = self.position
            df = pd.DataFrame(Position.find(query))
            df = df.fillna(0)
            result = df.to_dict('records')
            
            return {"status": True, "result": result}
        except Exception as e:
            print(e)
            return {"status": False, "error": e}

    def create(self, data):
        try:
            validate_res = ValidateDBData(self.schema, data)

            if not validate_res["status"]:
                return validate_res

            Position = self.position
            result = Position.insert_one(data)

            return {"status": True, "result": result}
        except Exception as e:
            print(e)
            return {"status": False, "error": e}   

            