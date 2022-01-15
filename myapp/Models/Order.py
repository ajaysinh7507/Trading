import pandas as pd
import bson
from myapp.Utils.mongodb import get_db_handle, get_collection_handle
from myapp.Utils.ValidateDBData import ValidateDBData


class Order:
    
    def __init__(self):
        self.db_handle = get_db_handle()
        self.order = get_collection_handle(self.db_handle, "order")

        self.schema = {
                        "kite_user_id": str,
                        "user_id": bson.objectId.ObjectId,
                        "script_id": bson.objectid.ObjectId, 
                        "variety": str,
                        "exchange": str,
                        "tradingsymbol": str, 
                        "instrument_token": str,
                        "quantity": str, 
                        "filled_quantity": str,
                        "pending_quantity": str,
                        "cancelled_quantity": str,
                        "product": str,
                        "order_type": str,
                        "price": str,
                        "trigger_price": str,
                        "average_price": str,
                        "order_id": str, 
                        "transaction_type": str, 
                        "trade_time": str, 
                        "trade_date": str, 
                        "status": str
                    }
    
    def getOne(self, query={}):
        try:
            Order = self.order
            result = Order.find_one(query)

            return {"status": True, "result": result}
        except Exception as e:
            print(e)
            return {"status": False, "error": e}
    
    def getAll(self, query={}, sort={}):
        try:
            Order = self.order
            df = pd.DataFrame(Order.find(query))
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

            Order = self.order
            result = Order.insert_one(data)

            return {"status": True, "result": result}
        except Exception as e:
            print(e)
            return {"status": False, "error": e}   

    def update(self, query, data):
        try:
            validate_res = ValidateDBData(self.schema, data)

            if not validate_res["status"]:
                return validate_res

            Order = self.order
            result = Order.update_one(query, data)

            return {"status": True, "result": result}
        except Exception as e:
            print(e)
            return {"status": False, "error": e}   

            