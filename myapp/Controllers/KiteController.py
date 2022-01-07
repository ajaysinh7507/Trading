import json
import numpy as np
import pandas as pd
import talib as ta
from datetime import timezone, datetime
from django.http import HttpResponse
from kiteconnect import KiteConnect

from myapp.Middlewares.AuthMiddlewareDecorator import isAuth

import myapp.Models.Script as ScriptClass
import myapp.Models.Order as OrderClass
class KiteController:

    # @isAuth()
    def getHistoricalData(request, script_instrument_token):
        
        api_key = "o40me2j1newtpkip"
        access_token = "5ki45xzI07WP3eOrBcdMPIqul9eOLulq"
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
            access_token = "5ki45xzI07WP3eOrBcdMPIqul9eOLulq"
            
            auth = request.auth
            body = request.POST
            
            quantity = int(body.get('quantity'))
            order_type = body.get('order_type').upper()
            price = body.get('price')
            transaction_type = body.get('transaction_type').upper()
            tradingsymbol = body.get('tradingsymbol')

            current_date = datetime.today().strftime('%Y-%m-%d')
            current_time = datetime.today().strftime("%H:%M:%S")
            
            variety = "regular"
            exchange = "NFO"
            product = "MIS"

            print("+++++++++ trading symbol +++++++++++++++++", tradingsymbol)

            script = ScriptClass.Script().getOne({"tradingsymbol": tradingsymbol})
            script = script["result"]
            
            
            # kite = KiteConnect(api_key)
            # kite.set_access_token(access_token)
            # order_id = kite.place_order(variety="regular", exchange="NFO", tradingsymbol=tradingsymbol, quantity=quantity, product='MIS', order_type=order_type, price=price, transaction_type=transaction_type)
            
            # order_data = {"user_id": auth['_id'], "script_id": script['_id'], "variety": variety, "exchange": exchange, "tradingsymbol": tradingsymbol, "quantity": quantity, "product": product, "order_type": order_type, "price": price, "order_id": order_id, "transaction_type": transaction_type, "trade_date": current_date, "trade_time": current_time, "status": True}

            # res = OrderClass.Order().create(order_data)
            # print(res)

            return HttpResponse(json.dumps({"status": True}), content_type='application/json')
        except Exception as e:
            print(e)

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
    
    