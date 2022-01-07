import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from datetime import datetime

from myapp.Middlewares.AuthMiddlewareDecorator import isAuth
import myapp.Models.Script as ScriptClass
class DemoController:
    def dashboard(request):
        current_date = datetime.today().strftime('%Y-%m-%d')
        
        script = ScriptClass.Script().getOne({"name": "BANKNIFTY", "expiry":{ "$gte": current_date }, "instrument_type": "FUT", "status": True})
        script = script["result"]
        return redirect('home.instrument_token', instrument_token=script['instrument_token'])

    def homeDashboard(request, instrument_token):
        
        return render(request, "index.html", {"script_instrument_token": instrument_token})

    @isAuth()
    def user(request):
        print(request)

        return HttpResponse(json.dumps({"status": True}), content_type='application/json')