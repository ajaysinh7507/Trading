import json
from re import sub
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
        
        script = ScriptClass.Script().getOne({"name": script_name, "expiry":{ "$gte": current_date }, "instrument_type": "FUT"})
        script = script['result']

        sub_script = ScriptClass.Script().getOne({"$query": {"name": script_name, "expiry":{ "$gte": current_date }, "instrument_type": {"$ne": "FUT"}}, "$orderby": { "expiry" : 1 }})
        sub_script = sub_script['result']
        sub_expiry = sub_script['expiry']

        instrument_tokens = ScriptClass.Script().getAll({"name": script_name, "instrument_type": {"$ne": "FUT"}, "expiry":sub_expiry})
        instrument_tokens = instrument_tokens['result']

        df = pd.DataFrame(instrument_tokens)
        tokens = df['instrument_token'].to_list()
        tokens.append(script['instrument_token'])
        script["all_tokens"] = tokens
        # script["all_tokens"] = script['all_tokens'].append(script['instrument_token'])
        script['next_thurs_expiry'] = sub_expiry
        
        value = json.dumps(json_util.dumps({"status": True, "response": script}), allow_nan=False)
        # print("data",len(value))
        return HttpResponse(value, content_type='application/json')