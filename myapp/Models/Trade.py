from cmath import isnan
import math
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
                        "sell_time": str,
                        "turnover": float,
                        "stt_total": float,
                        "etc": float,
                        "stax":  float,
                        "sebi_charges":  float,
                        "stamp_charges":  float,
                        "total_tax":  float,
                        "breakeven":  float,
                        "net_profit":  float,
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

    def calculateBrokerage(self, buy_price, sell_price, qty):
        brokerage = 40

        if math.isnan(buy_price) or buy_price == 0:
            buy_price = 0
            bse_tran_charge_buy = 0
            brokerage = 20
        
        if math.isnan(sell_price) or sell_price == 0:
            sell_price = 0
            bse_tran_charge_sell = 0
            brokerage = 20

        pnl = round(float((sell_price - buy_price) * qty), 2)
        turnover = round(float((buy_price + sell_price) * qty), 2)
        stt_total = round(float(sell_price * qty * 0.0005), 2)
        etc = round(float(0.00053 * turnover), 2)
        stax = round(float(0.18 * (brokerage + etc)), 2)
        sebi_charges = round(float(turnover * 0.000001), 2)
        stamp_charges = round(float(buy_price * qty * 0.00003), 2)
        total_tax = round(float(brokerage + stt_total + etc + stax + sebi_charges + stamp_charges), 2)
        breakeven = round(float(total_tax / qty), 2)
        breakeven =   0.0 if math.isnan(breakeven) else breakeven
        net_profit = round(float((pnl) - total_tax), 2)

        return { "pnl": pnl, "turnover": turnover, "stt_total": stt_total, "etc": etc, "stax": stax, "sebi_charges": sebi_charges, "stamp_charges": stamp_charges, "total_tax": total_tax, "breakeven": breakeven, "net_profit": net_profit }