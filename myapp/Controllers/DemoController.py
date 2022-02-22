import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from datetime import datetime

from myapp.Middlewares.AuthMiddlewareDecorator import isAuth
import myapp.Models.Script as ScriptClass
import myapp.Models.Trade as TradeClass
import myapp.Models.Order as OrderClass
class DemoController:
    
    @isAuth()
    def dashboard(request):
        current_date = datetime.today().strftime('%Y-%m-%d')
        
        script = ScriptClass.Script().getOne({"name": "BANKNIFTY", "expiry":{ "$gte": current_date }, "instrument_type": "FUT"})
        script = script["result"]
        
        return redirect('home.instrument_token', instrument_token=script['instrument_token'])
    
    @isAuth()
    def homeDashboard(request, instrument_token):
        try:
            auth = request.auth

            trades = TradeClass.Trade().getAll({"user_id": auth['_id']})
            if not trades["status"]:
                print("Error: ", trades)
            
            trades = trades['result']

            orders = OrderClass.Order().getAll({"user_id": auth['_id'], "square_off": "PENDING"})
            if not orders["status"]:
                print("Error: ", orders)
            
            orders = orders['result']

            return render(request, "index.html", {"script_instrument_token": instrument_token, "trades": trades, "orders": orders})
        except Exception as e:
            print(e)
            return 

    @isAuth()
    def user(request):
        print(request)

        return HttpResponse(json.dumps({"status": True}), content_type='application/json')