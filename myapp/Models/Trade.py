import pandas as pd
import bson
from myapp.Utils.mongodb import get_db_handle, get_collection_handle
from myapp.Utils.ValidateDBData import ValidateDBData

class Trade:
    
    def __init__(self):
        self.db_handle = get_db_handle()
        self.trade = get_collection_handle(self.db_handle, "trade")
        self.schema = {
                        "user_id": bson.objectid.ObjectId,
                        "order_id": str,
                        "kite_user_id": str,
                        "tradingsymbol": str,
                        "exchange": str,
                        "instrument_token": int,
                        "product": str,
                        "quantity": int,
                        "buy_price": float,
                        "sell_price": float,
                        "pnl": float,
                        "buy_date": str,
                        "buy_time": str,
                        "sell_date": str,
                        "sell_time": str
                    }

    def getOne(self, query={}):
        try:
            Trade = self.trade
            result = Trade.find_one(query)

            return {"status": True, "result": result}
        except Exception as e:
            print(e)
            return {"status": False, "error": e}
    
    def getAll(self, query={}, sort={}):
        try:
            Trade = self.trade
            df = pd.DataFrame(Trade.find(query))
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
            
            Trade = self.trade
            result = Trade.insert_one(data)
            
            return {"status": True, "result": result}
        except Exception as e:
            print(e)
            return {"status": False, "error": e}   

    def update(self, query, data):
        try:
            validate_res = ValidateDBData(self.schema, data)
            if not validate_res["status"]:
                return validate_res

            Trade = self.trade
            result = Trade.update_one(query, {"$set": data})

            return {"status": True, "result": result}
        except Exception as e:
            print(e)
            return {"status": False, "error": e}

            