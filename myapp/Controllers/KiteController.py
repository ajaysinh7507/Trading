
import os
import json
import numpy as np
import pandas as pd
import talib as ta
from bson import json_util, ObjectId
from datetime import timezone, datetime
from django.http import HttpResponse
from kiteconnect import KiteConnect

from myapp.Middlewares.AuthMiddlewareDecorator import isAuth

import myapp.Models.Script as ScriptClass
import myapp.Models.Order as OrderClass
import myapp.Models.Position as PositionClass
import myapp.Models.Trade as TradeClass
class KiteController:

    # @isAuth()
    def getHistoricalData(request, script_instrument_token):
        
        api_key = "o40me2j1newtpkip"
        access_token = "b3kDWd4fhRWNlGTagHsAH0xC4cDnpD5E"
        interval = "minute"

        instrument_token = script_instrument_token
        from_date = request.GET.get('date', '')+" "+request.GET.get('time', '')
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")
        to_date = current_date+" "+current_time if current_time <= "15:29:00" else current_date+" "+"15:29:00"
        
        kite = KiteConnect(api_key)
        kite.set_access_token(access_token)
        
        historical_data = kite.historical_data(instrument_token, from_date, to_date, interval)
        
        df = pd.DataFrame(historical_data)
        
        bollinger_band = ta.BBANDS(df['close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0 )
        bb_u = bollinger_band[0].to_numpy()
        bb_m = bollinger_band[1].to_numpy()
        bb_l = bollinger_band[2].to_numpy() 

        ema_7 = ta.EMA(df['close'], 7).to_numpy()
        ema_21 = ta.EMA(df['close'], 21).to_numpy()
        ema_50 = ta.EMA(df['close'], 50).to_numpy()

        stoch = ta.STOCH(df['high'], df['low'], df['close'], fastk_period=14, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)        
        stoch_k = stoch[0].to_numpy()
        stoch_d = stoch[1].to_numpy()

        obj = KiteController()
        formated_data = obj.formatHistoricalData(historical_data, bb_u, bb_m, bb_l, ema_7, ema_21, ema_50, stoch_k, stoch_d)

        script = ScriptClass.Script().getOne({"instrument_token": instrument_token})
        script = script['result']
        
        return HttpResponse(json.dumps({"instrument": script['tradingsymbol'],"data":formated_data}), content_type='application/json')
    
    @isAuth()
    def orderPlace(request):
        try:
            api_key = "o40me2j1newtpkip"
            access_token = "b3kDWd4fhRWNlGTagHsAH0xC4cDnpD5E"
            
            auth = request.auth
            body = request.POST
            
            quantity = int(body.get('quantity'))
            order_type = body.get('order_type').upper()
            price = float(body.get('price'))
            transaction_type = body.get('transaction_type').upper()
            tradingsymbol = body.get('tradingsymbol')

            current_date = datetime.today().strftime('%Y-%m-%d')
            current_time = datetime.today().strftime("%H:%M:%S")
            
            variety = "regular"
            exchange = "NFO"
            product = "MIS"

            script = ScriptClass.Script().getOne({"tradingsymbol": tradingsymbol})
            script = script["result"]
            
            kite = KiteConnect(api_key)
            kite.set_access_token(access_token)
            # order_id = kite.place_order(variety="regular", exchange="NFO", tradingsymbol=tradingsymbol, quantity=quantity, product='MIS', order_type=order_type, price=price, transaction_type=transaction_type)
            order_id = "123456"
            
            order_data = {"user_id": auth['_id'], "script_id": script['_id'], "variety": variety, "exchange": exchange, "tradingsymbol": tradingsymbol, "instrument_token": script["instrument_token"], "quantity": quantity, "product": product, "order_type": order_type, "price": price, "order_id": order_id, "transaction_type": transaction_type, "trade_date": current_date, "trade_time": current_time, "remaining_quantity": quantity, "square_off": "PENDING", "status": "PENDING"}
            
            res = OrderClass.Order().create(order_data)
            
            if not res['status']: 
                return HttpResponse(json.dumps({"status": False, "message": res['error']}), content_type='application/json')

            return HttpResponse(json.dumps({"status": True, "message": "order placed"}), content_type='application/json')
        except Exception as e:
            print(e)

    def orderPostBack(request):
        api_key = "o40me2j1newtpkip"
        access_token = "b3kDWd4fhRWNlGTagHsAH0xC4cDnpD5E"

        current_date = datetime.today().strftime('%Y-%m-%d')
        current_time = datetime.today().strftime("%H:%M:%S")

        body = request.POST
        kite_user_id = body['user_id']
        order_id = body['order_id']
        status = body['status']
        order_timestamp = body['order_timestamp']
        quantity = abs(int(body['quantity']))
        pending_quantity = abs(int(body['pending_quantity']))
        filled_quantity = abs(int(body['filled_quantity']))
        cancelled_quantity = abs(int(body['cancelled_quantity']))
        price = float(body['price'])
        trigger_price = float(body['trigger_price'])
        average_price = float(body['average_price'])
        instrument_token = int(body['instrument_token'])
        tradingsymbol = body['tradingsymbol']
        transaction_type = body['transaction_type']
        exchange = body['exchange']
        product = body['product']
        profit = "null"
        limit_profit = "null"
        stoploss = "null"

        if not os.path.exists(os.path.join("myapp","static","post_back_logs")):
            os.mkdir(os.path.join("myapp","static","post_back_logs"))
        
        f = open(os.path.join("myapp","static","post_back_logs", order_id+".text"), 'a')
        logs_list = ["\n\n\n=============================="+current_date+" "+current_time+"==============================\n", json.dumps(request.POST)]

        order = OrderClass.Order().getOne({"order_id": order_id})
        order = order["result"]

        if not order or order is None:
            logs_list.append("\n=>ORDER NOT FOUND")
            f.writelines(logs_list)
            f.close()
            print("order not found")
            
            return HttpResponse(json.dumps({"status": False}), content_type='application/json')

        user_id = order["user_id"]
        
        update_order = OrderClass.Order().update({"order_id": order_id}, {"kite_user_id": kite_user_id, "filled_quantity": filled_quantity, "pending_quantity": pending_quantity, "cancelled_quantity": cancelled_quantity,"trigger_price": trigger_price, "price": price, "average_price":average_price, "order_timestamp": order_timestamp,"status": status})

        if not update_order["status"]:
            print(update_order)
            logs_list.append("\n=>There is problem to update order with status"+status)
            f.writelines(logs_list)
            f.close()
            
            return HttpResponse(json.dumps({"status": False}), content_type='application/json')
            
        logs_list.append("\n=>Order updated with status"+status)

        old_orders = OrderClass.Order().getAll({"user_id": user_id, "transaction_type": "SELL" if transaction_type == "BUY" else "BUY", "instrument_token": instrument_token, "tradingsymbol": tradingsymbol, "square_off": "PENDING", "status": "COMPLETE"}, [("order_timestamp", 1)])

        if not old_orders["status"]:
            print(old_orders)
            logs_list.append("\n=>There is problem to get all old order with status"+str(old_orders))
            f.writelines(logs_list)
            f.close()
            
            return HttpResponse(json.dumps({"status": False}), content_type='application/json')

        old_orders = old_orders["result"]
        
        if len(old_orders) > 0:
            total_qty = quantity
            
            for old_order in old_orders:
                if old_order["transaction_type"] == "BUY":
                    buy_price = old_order["average_price"]
                    buy_time = old_order["order_timestamp"]
                    sell_price = average_price
                    sell_time = order_timestamp
                else:
                    buy_price = average_price
                    buy_time = order_timestamp
                    sell_price = old_order["average_price"]
                    sell_time = old_order["order_timestamp"]
                    
                if old_order["remaining_quantity"] < total_qty:
                    OrderClass.Order().update({"order_id": old_order['order_id']}, {"square_off": "COMPLETE", "remaining_quantity": 0})
                    
                    trade_data = { "user_id": user_id, "kite_user_id": kite_user_id, "order_id": order_id, "tradingsymbol": tradingsymbol, "exchange": exchange, "instrument_token": instrument_token, "product": product, "quantity":old_order["remaining_quantity"], "buy_price": buy_price, "sell_price": sell_price, "buy_time": buy_time, "sell_time": sell_time }
                    
                    TradeClass.Trade().create(trade_data)
                else:
                    order_remaining_qty = old_order["remaining_quantity"] - total_qty
                    OrderClass.Order().update({"order_id": old_order['order_id']}, {"remaining_quantity": order_remaining_qty})
                    
                    trade_data = { "user_id": user_id, "kite_user_id": kite_user_id, "order_id": order_id, "tradingsymbol": tradingsymbol, "exchange": exchange, "instrument_token": instrument_token, "product": product, "quantity":total_qty, "buy_price": buy_price, "sell_price": sell_price, "buy_time": buy_time, "sell_time": sell_time }
                    
                    TradeClass.Trade().create(trade_data)
                
                total_qty -= old_order["remaining_quantity"]
                if(total_qty <= 0): continue
            
            if total_qty > 0:
                OrderClass.Order().update({"order_id": order_id}, {"remaining_quantity": total_qty})
            else:
                OrderClass.Order().update({"order_id": order_id}, {"square_off": "COMPLETE", "remaining_quantity": 0})

        position = PositionClass.Position().getOne({"user_id": user_id, "tradingsymbol": tradingsymbol, "status": "PENDING"})
        position = position["result"]

        if not position or position is None:
            position_data = {"user_id": user_id, "tradingsymbol": tradingsymbol, "exchange": exchange, "instrument_token": instrument_token, "product": product, "pnl": 0.0, "date_time": order_timestamp, "status": "PENDING"}

            if transaction_type == "SELL":
                position_data['buy_quantity'] = 0
                position_data['buy_price'] = 0.0
                position_data['sell_price'] = average_price
                position_data['sell_quantity'] = quantity
                position_data['quantity'] = 0-quantity
            else:
                position_data['buy_price'] = average_price
                position_data['buy_quantity'] = quantity
                position_data['sell_price'] = 0.0
                position_data['sell_quantity'] = 0
                position_data['quantity'] = quantity
            
            create_position_res = PositionClass.Position().create(position_data)
            if not create_position_res["status"]:  
                print(create_position_res)
                logs_list.append("\n=>There is problem to insert new position record"+json.dumps(json_util.dumps(position_data)))
        else:
            pos_sell_qty = position['sell_quantity']
            pos_sell_price = position['sell_price']
            pos_buy_qty = position['buy_quantity']
            pos_buy_price = position['buy_price']
            pos_total_qty = position['quantity']

            if transaction_type == "SELL":
                buy_time = position['date_time']   
                sell_time = order_timestamp

                average = ((pos_sell_qty * pos_sell_price) + (quantity * average_price)) / (pos_sell_qty + quantity)
                position['sell_quantity'] += quantity
                position['sell_price'] = average
                position['quantity'] -= quantity
                position['date_time'] = sell_time
            else:
                buy_time = order_timestamp
                sell_time = position['date_time']

                average = ((pos_buy_qty * pos_buy_price) + (quantity * average_price)) / (pos_buy_qty + quantity)
                position['buy_quantity'] += quantity
                position['buy_price'] = average
                position['quantity'] += quantity
                position['date_time'] = buy_time
			
            if position['quantity'] == 0:
                newPNL = (pos_sell_price - pos_buy_price) * position['quantity']
                position['pnl'] += newPNL
                position['status'] = "COMPLETED"
                position['sell_quantity'] = 0
                position['sell_price'] = 0.0
                position['quantity'] = 0
                position['buy_quantity'] = 0
                position['buy_price'] = 0.0
                position['quantity'] = 0

            del position['_id']
            
            update_position_res = PositionClass.Position().update({"user_id": user_id, "tradingsymbol": tradingsymbol}, position)
            if not update_position_res["status"]:  
                print(update_position_res)
                logs_list.append("\n=>There is problem to insert new position record"+json.dumps(json_util.dumps(position)))

            # if abs(position['quantity']) < abs(pos_total_qty):
            #     trade_data = { "user_id": user_id, "tradingsymbol": tradingsymbol, "exchange": exchange, "instrument_token": instrument_token, "product": product, "quantity":abs(position['quantity']), "buy_price": position['buy_price'], "sell_price": position['sell_price'], "buy_time": buy_time, "sell_time": sell_time }
            #     create_trade_res = TradeClass.Trade().create(trade_data)

            #     if not create_trade_res["status"]:  
            #         print(update_position_res)
            #         logs_list.append("\n=>There is problem to insert new trade record"+json.dumps(json_util.dumps(create_trade_res)))
		
        script_id = order["script_id"]
        
        # kite = KiteConnect(api_key)
        # kite.set_access_token(access_token)   
        # positions = kite.positions()
        
        # if len(positions["net"]) > 0:

        #     for pos in positions["net"]:
                
        #         if pos["quantity"] == 0 and pos["instrument_token"] == instrument_token:
                    

        
        logs_list.append("\n=>SUCCESSFULLY DONE")
        f.writelines(logs_list)
        f.close()
        return HttpResponse(json.dumps({"status": True}), content_type='application/json')


    def formatHistoricalData(request, datas, bb_u, bb_m, bb_l, ema_7, ema_21, ema_50, stoch_k, stoch_d):
        
        candle_data_arr = []
        volume_data_arr = []

        bb_u_data_arr = []
        bb_m_data_arr = []
        bb_l_data_arr = []

        ema_7_data_arr = []
        ema_21_data_arr = []
        ema_50_data_arr = []

        stoch_k_data_arr = []
        stoch_d_data_arr = []

        i = 0
        for data in datas:
            open = data['open']
            high = data['high']
            low = data['low']
            close = data['close']
            volume = data['volume']

            date_timestamp = data['date'].replace(tzinfo=timezone.utc)
            date_timestamp = int(date_timestamp.timestamp())*1000
            
            candle_data_arr.append([date_timestamp, open, high, low, close])
            volume_data_arr.append([date_timestamp, volume])
            
            if not np.isnan(bb_u[i]): bb_u_data_arr.append([date_timestamp, bb_u[i]])
            if not np.isnan(bb_m[i]): bb_m_data_arr.append([date_timestamp, bb_m[i]])
            if not np.isnan(bb_l[i]): bb_l_data_arr.append([date_timestamp, bb_l[i]])

            if not np.isnan(ema_7[i]): ema_7_data_arr.append([date_timestamp, ema_7[i]])
            if not np.isnan(ema_21[i]): ema_21_data_arr.append([date_timestamp, ema_21[i]])
            if not np.isnan(ema_50[i]): ema_50_data_arr.append([date_timestamp, ema_50[i]])

            if not np.isnan(stoch_k[i]) : stoch_k_data_arr.append([date_timestamp, stoch_k[i]])
            if not np.isnan(stoch_d[i]) : stoch_d_data_arr.append([date_timestamp, stoch_d[i]])
        
            i += 1

        bb_data = {'bb_u':  bb_u_data_arr, 'bb_m': bb_m_data_arr, 'bb_l': bb_l_data_arr}
        ema_data = {'ema_7': ema_7_data_arr, 'ema_21': ema_21_data_arr, 'ema_50': ema_50_data_arr}
        stoch_data = {'stoch_k': stoch_k_data_arr, 'stoch_d': stoch_d_data_arr}

        return {'candle_data': candle_data_arr, 'volume_data': volume_data_arr, 'bb_data': bb_data, 'ema_data': ema_data, 'stoch_data': stoch_data}
        # return {'candle_data': candle_data_arr, 'volume_data': volume_data_arr, 'bb_u_data':  bb_u_data_arr, 'bb_m_data': bb_m_data_arr, 'bb_l_data': bb_l_data_arr, 'ema_7_data': ema_7_data_arr, 'ema_21_data': ema_21_data_arr, 'ema_50_data': ema_50_data_arr, 'stoch_k_data': stoch_k_data_arr, 'stoch_d_data': stoch_d_data_arr}
    
    