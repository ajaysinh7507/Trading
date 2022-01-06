import json
import pandas as pd
import numpy as np
from os import name
from bson import json_util, ObjectId
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime

from myapp.Middlewares.AuthMiddlewareDecorator import isAuth
import myapp.Models.Script as ScriptClass

class ScriptController:
    
    def getScript(request):
        script_name = request.GET.get('script_name')
        current_date = datetime.today().strftime('%Y-%m-%d')
        
        script = ScriptClass.Script().getOne({"name": script_name, "expiry":{ "$gte": current_date }, "instrument_type": "FUT", "status": True})
        script = script['result']

        instrument_tokens = ScriptClass.Script().getAll({"name": script_name, "expiry":{ "$gte": current_date }})
        instrument_tokens = instrument_tokens['result']

        df = pd.DataFrame(instrument_tokens)
        script["all_tokens"] = df['instrument_token'].to_list()
        
        value = json.dumps(json_util.dumps({"status": True, "response": script}), allow_nan=False)
        # print("data",len(value))
        return HttpResponse(value, content_type='application/json')