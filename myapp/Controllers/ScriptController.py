import json
from bson import json_util, ObjectId
from django.http import HttpResponse
from django.shortcuts import render

from myapp.Middlewares.AuthMiddlewareDecorator import isAuth
import myapp.Models.Script as ScriptClass

class ScriptController:
    
    def getAllScript(request):
        scripts = ScriptClass.Script().getAll({"status": True})
        
        value = json.dumps(json_util.dumps(scripts), allow_nan=False)
        # print("data",len(value))
        return HttpResponse(value, content_type='application/json')